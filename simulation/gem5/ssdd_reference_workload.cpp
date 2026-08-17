#include <array>
#include <atomic>
#include <cinttypes>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <cstdio>

namespace {

constexpr std::uint64_t kSeed = 0x535344445F563132ULL;
constexpr int kStages = 5;
constexpr int kEngines = 7;
constexpr std::size_t kProbeWords = 8192;

struct Record {
  std::uint64_t sequence;
  std::uint64_t state;
  std::uint64_t proof;
};

std::uint64_t mix(std::uint64_t value) {
  value ^= value >> 30;
  value *= 0xBF58476D1CE4E5B9ULL;
  value ^= value >> 27;
  value *= 0x94D049BB133111EBULL;
  return value ^ (value >> 31);
}

std::uint64_t recordProof(std::uint64_t sequence, std::uint64_t state) {
  return mix(kSeed ^ (sequence * 0x9E3779B97F4A7C15ULL) ^ state);
}

}  // namespace

int main(int argc, char* argv[]) {
  bool injectProofCorruption = false;
  std::size_t faultRecord = 18;
  for (int arg = 1; arg < argc; ++arg) {
    if (std::strcmp(argv[arg], "--fault=proof-corruption") == 0) {
      injectProofCorruption = true;
    } else if (std::strncmp(argv[arg], "--fault-record=", 15) == 0) {
      const char* value = argv[arg] + 15;
      char* end = nullptr;
      const unsigned long parsed = std::strtoul(value, &end, 10);
      if (*value == '\0' || *end != '\0' || parsed < 1 || parsed > kStages * kEngines) {
        std::fprintf(stderr, "fault record must be within 1..%d\n", kStages * kEngines);
        return 64;
      }
      faultRecord = static_cast<std::size_t>(parsed);
    } else if (std::strcmp(argv[arg], "--fault=none") != 0) {
      std::fprintf(stderr, "unknown argument: %s\n", argv[arg]);
      return 64;
    }
  }

  std::array<Record, kStages * kEngines> journal{};
  std::array<std::uint64_t, kProbeWords> memoryProbeBuffer{};
  std::uint64_t digest = kSeed;
  std::uint64_t memoryProbe = kSeed;
  std::size_t cursor = 0;

  // Deliberately exceed the 32 KiB L1 data cache used by the gem5 experiment.
  // This is a model-local timing probe, not a hardware performance benchmark.
  for (std::size_t index = 0; index < memoryProbeBuffer.size(); ++index) {
    memoryProbeBuffer[index] = mix(kSeed ^ index);
  }
  for (std::size_t pass = 0; pass < 4; ++pass) {
    for (std::size_t index = 0; index < memoryProbeBuffer.size(); ++index) {
      const std::size_t probeIndex = (index * 4051 + pass * 977) & (kProbeWords - 1);
      memoryProbe = mix(memoryProbe ^ memoryProbeBuffer[probeIndex]);
    }
  }

  for (int stage = 1; stage <= kStages; ++stage) {
    for (int engine = 1; engine <= kEngines; ++engine) {
      const std::uint64_t sequence = static_cast<std::uint64_t>(cursor + 1);
      const std::uint64_t state =
          (static_cast<std::uint64_t>(stage) << 32) | static_cast<std::uint64_t>(engine);
      const std::uint64_t proof = recordProof(sequence, state);

      journal[cursor] = {sequence, state, proof};
      std::atomic_thread_fence(std::memory_order_seq_cst);
      digest = mix(digest ^ proof ^ (sequence << 1));
      ++cursor;
    }
  }

  if (injectProofCorruption) {
    // A controlled fault changes one journal proof after the canonical trace
    // has been assembled. The validator should reject this specific mutation.
    journal[faultRecord - 1].proof ^= 0x1ULL;
  }

  bool accepted = true;
  std::uint64_t observedDigest = kSeed;
  for (const auto& record : journal) {
    if (record.proof != recordProof(record.sequence, record.state)) {
      accepted = false;
    }
    observedDigest = mix(observedDigest ^ record.proof ^ (record.sequence << 1));
  }

  std::printf("SSDD_REFERENCE_WORKLOAD v0.1\n");
  std::printf("stages=%d engines=%d operations=%zu\n", kStages, kEngines, cursor);
  std::printf("replay_digest=%016" PRIx64 "\n", observedDigest);
  std::printf("reference_digest=%016" PRIx64 "\n", digest);
  std::printf("memory_probe=%016" PRIx64 "\n", memoryProbe);
  std::printf("fault_mode=%s\n", injectProofCorruption ? "proof-corruption" : "none");
  std::printf("fault_record=%zu\n", injectProofCorruption ? faultRecord : 0);
  std::printf("validation=%s\n", accepted ? "accepted" : "rejected");
  return accepted ? 0 : 2;
}
