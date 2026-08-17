#!/usr/bin/env python3

# SSDD deterministic engine - implements the five- stage pipeline:
# SSC (ordering) → Aggregation → Fusion → Ledger
# Also includes physics constraints and deterministic RNG.
# All operations are deterministic and bit- identical across runs.

import hashlib
import struct
import numpy as np
from typing import List, Tuple, Dict, Any
from q32_32_core import double_to_q32, q32_to_double, q32_add_sat, q32_mul_sat

# Packet definition with quadruple key
#
class Packet:
    def __init__(self, structural_dim: int, enterprise_type: int, seq: int, source_chiplet_id: int, payload: Any = None):
        self.structural_dim = structural_dim
        self.enterprise_type = enterprise_type
        self.seq = seq
        self.source_chiplet_id = source_chiplet_id
        self.payload = payload

    def __lt__(self, other):
        """Lexicographic ordering using the quadruple key."""
        return ((self.structural_dim, self.enterprise_type, self.seq, self.source_chiplet_id) <
                (other.structural_dim, other.enterprise_type, other.seq, other.source_chiplet_id))

# Sovereign Sidecar (SSC)
#
class SovereignSidecar:
    def __init__(self, time_window_cycles: int):
        self.window = []   # list of (cycle, packet)
        self.time_window_cycles = time_window_cycles
        self.current_cycle = 0

    def receive_packet(self, packet: Packet, cycle: int):
        self.window.append((cycle, packet))

    def emit_sorted_batch(self, cycle: int) -> List[Packet]:
        """Emit packets that have aged out of the window, sorted by quadruple key."""
        # Remove packets still inside the window
        batch = [p for c, p in self.window if c <= cycle - self.time_window_cycles]
        # Keep only packets that remain in the window for next cycle
        self.window = [(c, p) for c, p in self.window if c > cycle - self.time_window_cycles]
        # Deterministic sort using the quadruple key
        batch.sort()   # relies on Packet.__lt__
        return batch

    def advance_cycle(self):
        self.current_cycle += 1

# Aggregation Furnace - commutative and associative reduction
#
class AggregationFurnace:
    def __init__(self, fid: int):
        self.id = fid
        self.aggregated_value = 0   # Q32.32 integer

    def add(self, packet: Packet):
        # For demonstration, we simply sum the sequence numbers (commutative)
        # In the real system, this would be a deterministic state reduction.
        self.aggregated_value = q32_add_sat(self.aggregated_value, packet.seq)

    def get_value(self) -> int:
        return self.aggregated_value

# Fusion Furnace - deterministic merge of aggregated fragments
#
class FusionFurnace:
    def __init__(self, fid: int):
        self.id = fid
        self.global_state = 0

    def fuse(self, aggregates: List[int]):
        # Deterministic merge: sum all aggregates (commutative, associative)
        total = 0
        for v in aggregates:
            total = q32_add_sat(total, v)
        self.global_state = total

    def get_state(self) -> int:
        return self.global_state

# Sovereign Ledger
#
class SovereignLedger:
    def __init__(self, genesis_hash: bytes):
        self.chain = [genesis_hash]   # list of hash bytes
        self.audit_trail = []          # list of (epoch_id, state_hash, prev_hash, agg)
        self.snapshot_hash = genesis_hash

    def commit(self, epoch_id: int, global_state: int, prev_hash: bytes) -> bytes:
        # Serialize the state (simplified: just the integer in big‑endian)
        state_bytes = struct.pack('>q', global_state)   # Q32.32 as signed 64‑bit
        # Compute new hash
        new_hash = hashlib.sha256(prev_hash + state_bytes).digest()
        self.chain.append(new_hash)
        # Append to audit trail
        self.audit_trail.append((epoch_id, new_hash, prev_hash, global_state))
        return new_hash

    def write_audit_trail(self, filename: str = "audit_trail.bin"):
        """Write binary audit trail according to the specification."""
        with open(filename, 'wb') as f:
            for epoch_id, state_hash, prev_hash, agg in self.audit_trail:
                f.write(struct.pack('>Q', epoch_id))     # epoch_id
                f.write(state_hash)                      # 32 bytes
                f.write(prev_hash)                       # 32 bytes
                f.write(struct.pack('>q', agg))          # aggregate (Q32.32)
        print(f"Audit trail written to {filename}")

# ----------------------------------------------------------------------
# Physics constraints (timing and amplitude)
# ----------------------------------------------------------------------
class PhysicsConstraints:
    T_DECISION = 73e-12   # 73 ps
    A_MAX = 0.05

    def check(self, latency: float, amplitude: float) -> bool:
        if latency > self.T_DECISION:
            return False
        if amplitude > self.A_MAX:
            return False
        return True

# ----------------------------------------------------------------------
# Xorshift128 deterministic RNG
# ----------------------------------------------------------------------
class Xorshift128:
    def __init__(self, seed: int):
        self.state = seed & ((1 << 128) - 1)

    def next(self) -> int:
        self.state ^= (self.state << 23) & ((1 << 128) - 1)
        self.state ^= (self.state >> 17)
        self.state ^= (self.state << 26)
        return (self.state >> 32) & 0xFFFFFFFF

    def uniform(self, low: float = 0.0, high: float = 1.0) -> float:
        """Return a uniform float in [low, high)."""
        return low + (self.next() / (1 << 32)) * (high - low)

    def normal(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        """Box‑Muller transform for Gaussian noise."""
        u1 = self.uniform()
        u2 = self.uniform()
        z = np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * np.pi * u2)
        return mu + z * sigma

def deterministic_rng(epoch_id: int, snapshot_hash: bytes) -> Xorshift128:
    seed_material = str(epoch_id).encode() + snapshot_hash
    seed = int.from_bytes(hashlib.sha256(seed_material).digest(), 'big')
    return Xorshift128(seed)