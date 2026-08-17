// Bounded Snapshot / Epoch Sequencing and Sorting Controller (SSC).
//
// Scope: RTL-simulation candidate for deterministic packet ordering only.
// This module does not implement aggregation, hashing, CXL, persistence,
// timing closure, FPGA integration, or a production SSDD runtime.
module snapshot_epoch_ssc #(
    parameter integer CAPACITY = 8
) (
    input  logic               clk,
    input  logic               reset_n,
    input  logic               snapshot_begin,
    input  logic               packet_valid,
    input  logic [31:0]        structural_dim,
    input  logic [31:0]        enterprise_type,
    input  logic [31:0]        sequence_id,
    input  logic [31:0]        source_chiplet_id,
    input  logic signed [63:0] payload_q32,
    input  logic [31:0]        node_id,
    input  logic               snapshot_close,
    output logic               snapshot_active,
    output logic               snapshot_rejected,
    output logic               out_valid,
    input  logic               out_ready,
    output logic [31:0]        out_structural_dim,
    output logic [31:0]        out_enterprise_type,
    output logic [31:0]        out_sequence_id,
    output logic [31:0]        out_source_chiplet_id,
    output logic signed [63:0] out_payload_q32,
    output logic [31:0]        out_node_id
);

    logic [31:0] stored_structural_dim [0:CAPACITY-1];
    logic [31:0] stored_enterprise_type [0:CAPACITY-1];
    logic [31:0] stored_sequence_id [0:CAPACITY-1];
    logic [31:0] stored_source_chiplet_id [0:CAPACITY-1];
    logic signed [63:0] stored_payload_q32 [0:CAPACITY-1];
    logic [31:0] stored_node_id [0:CAPACITY-1];

    integer packet_count;
    integer output_index;
    logic output_active;
    integer i;
    integer j;
    logic duplicate_found;
    logic [31:0] swap_structural_dim;
    logic [31:0] swap_enterprise_type;
    logic [31:0] swap_sequence_id;
    logic [31:0] swap_source_chiplet_id;
    logic signed [63:0] swap_payload_q32;
    logic [31:0] swap_node_id;

    function automatic key_less(
        input logic [31:0] left_structural_dim,
        input logic [31:0] left_enterprise_type,
        input logic [31:0] left_sequence_id,
        input logic [31:0] left_source_chiplet_id,
        input logic [31:0] right_structural_dim,
        input logic [31:0] right_enterprise_type,
        input logic [31:0] right_sequence_id,
        input logic [31:0] right_source_chiplet_id
    );
        begin
            if (left_structural_dim != right_structural_dim)
                key_less = left_structural_dim < right_structural_dim;
            else if (left_enterprise_type != right_enterprise_type)
                key_less = left_enterprise_type < right_enterprise_type;
            else if (left_sequence_id != right_sequence_id)
                key_less = left_sequence_id < right_sequence_id;
            else
                key_less = left_source_chiplet_id < right_source_chiplet_id;
        end
    endfunction

    always_comb begin
        out_valid = output_active;
        out_structural_dim = '0;
        out_enterprise_type = '0;
        out_sequence_id = '0;
        out_source_chiplet_id = '0;
        out_payload_q32 = '0;
        out_node_id = '0;
        if (output_active) begin
            out_structural_dim = stored_structural_dim[output_index];
            out_enterprise_type = stored_enterprise_type[output_index];
            out_sequence_id = stored_sequence_id[output_index];
            out_source_chiplet_id = stored_source_chiplet_id[output_index];
            out_payload_q32 = stored_payload_q32[output_index];
            out_node_id = stored_node_id[output_index];
        end
    end

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            snapshot_active <= 1'b0;
            snapshot_rejected <= 1'b0;
            packet_count <= 0;
            output_index <= 0;
            output_active <= 1'b0;
        end else if (snapshot_begin) begin
            snapshot_active <= 1'b1;
            snapshot_rejected <= 1'b0;
            packet_count <= 0;
            output_index <= 0;
            output_active <= 1'b0;
        end else begin
            if (packet_valid && snapshot_active && !snapshot_rejected) begin
                duplicate_found = 1'b0;
                for (i = 0; i < CAPACITY; i = i + 1) begin
                    if ((i < packet_count) &&
                        (stored_structural_dim[i] == structural_dim) &&
                        (stored_enterprise_type[i] == enterprise_type) &&
                        (stored_sequence_id[i] == sequence_id) &&
                        (stored_source_chiplet_id[i] == source_chiplet_id)) begin
                        duplicate_found = 1'b1;
                    end
                end
                if (duplicate_found || packet_count >= CAPACITY) begin
                    snapshot_rejected <= 1'b1;
                end else begin
                    stored_structural_dim[packet_count] <= structural_dim;
                    stored_enterprise_type[packet_count] <= enterprise_type;
                    stored_sequence_id[packet_count] <= sequence_id;
                    stored_source_chiplet_id[packet_count] <= source_chiplet_id;
                    stored_payload_q32[packet_count] <= payload_q32;
                    stored_node_id[packet_count] <= node_id;
                    packet_count <= packet_count + 1;
                end
            end

            if (snapshot_close && snapshot_active) begin
                snapshot_active <= 1'b0;
                if (!snapshot_rejected) begin
                    for (i = 0; i < CAPACITY - 1; i = i + 1) begin
                        for (j = 0; j < CAPACITY - 1 - i; j = j + 1) begin
                            if ((j + 1 < packet_count) &&
                                key_less(
                                    stored_structural_dim[j + 1],
                                    stored_enterprise_type[j + 1],
                                    stored_sequence_id[j + 1],
                                    stored_source_chiplet_id[j + 1],
                                    stored_structural_dim[j],
                                    stored_enterprise_type[j],
                                    stored_sequence_id[j],
                                    stored_source_chiplet_id[j])) begin
                                swap_structural_dim = stored_structural_dim[j];
                                swap_enterprise_type = stored_enterprise_type[j];
                                swap_sequence_id = stored_sequence_id[j];
                                swap_source_chiplet_id = stored_source_chiplet_id[j];
                                swap_payload_q32 = stored_payload_q32[j];
                                swap_node_id = stored_node_id[j];
                                stored_structural_dim[j] = stored_structural_dim[j + 1];
                                stored_enterprise_type[j] = stored_enterprise_type[j + 1];
                                stored_sequence_id[j] = stored_sequence_id[j + 1];
                                stored_source_chiplet_id[j] = stored_source_chiplet_id[j + 1];
                                stored_payload_q32[j] = stored_payload_q32[j + 1];
                                stored_node_id[j] = stored_node_id[j + 1];
                                stored_structural_dim[j + 1] = swap_structural_dim;
                                stored_enterprise_type[j + 1] = swap_enterprise_type;
                                stored_sequence_id[j + 1] = swap_sequence_id;
                                stored_source_chiplet_id[j + 1] = swap_source_chiplet_id;
                                stored_payload_q32[j + 1] = swap_payload_q32;
                                stored_node_id[j + 1] = swap_node_id;
                            end
                        end
                    end
                    output_index <= 0;
                    output_active <= packet_count != 0;
                end
            end

            if (output_active && out_ready) begin
                if (output_index + 1 >= packet_count) begin
                    output_active <= 1'b0;
                    output_index <= 0;
                end else begin
                    output_index <= output_index + 1;
                end
            end
        end
    end
endmodule
