`timescale 1ns/1ps

module tb_snapshot_epoch_ssc;
    localparam integer COUNT = 8;
    logic clk = 1'b0;
    logic reset_n = 1'b0;
    logic snapshot_begin = 1'b0;
    logic packet_valid = 1'b0;
    logic [31:0] structural_dim = '0;
    logic [31:0] enterprise_type = '0;
    logic [31:0] sequence_id = '0;
    logic [31:0] source_chiplet_id = '0;
    logic signed [63:0] payload_q32 = '0;
    logic [31:0] node_id = '0;
    logic snapshot_close = 1'b0;
    logic snapshot_active;
    logic snapshot_rejected;
    logic out_valid;
    logic out_ready = 1'b1;
    logic [31:0] out_structural_dim;
    logic [31:0] out_enterprise_type;
    logic [31:0] out_sequence_id;
    logic [31:0] out_source_chiplet_id;
    logic signed [63:0] out_payload_q32;
    logic [31:0] out_node_id;
    integer failures = 0;
    integer trial;
    integer item;
    integer received;
    integer actual_id;
    integer rotation;

    logic [31:0] in_structural_dim [0:COUNT-1];
    logic [31:0] in_enterprise_type [0:COUNT-1];
    logic [31:0] in_sequence_id [0:COUNT-1];
    logic [31:0] in_source_chiplet_id [0:COUNT-1];
    logic signed [63:0] in_payload_q32 [0:COUNT-1];
    logic [31:0] in_node_id [0:COUNT-1];
    integer expected_id [0:COUNT-1];

    snapshot_epoch_ssc #(.CAPACITY(COUNT)) dut (
        .clk, .reset_n, .snapshot_begin, .packet_valid,
        .structural_dim, .enterprise_type, .sequence_id, .source_chiplet_id,
        .payload_q32, .node_id, .snapshot_close, .snapshot_active,
        .snapshot_rejected, .out_valid, .out_ready, .out_structural_dim,
        .out_enterprise_type, .out_sequence_id, .out_source_chiplet_id,
        .out_payload_q32, .out_node_id
    );

    always #5 clk = ~clk;

    task automatic assert_true(input logic condition, input string label);
        begin
            if (!condition) begin
                failures = failures + 1;
                $display("RTL_SSC_ASSERT_FAIL %s at %0t", label, $time);
            end
        end
    endtask

    task automatic setup_main_vector;
        begin
            // Deliberately not in canonical order.
            in_structural_dim[0] = 2; in_enterprise_type[0] = 1; in_sequence_id[0] = 3; in_source_chiplet_id[0] = 7;
            in_structural_dim[1] = 0; in_enterprise_type[1] = 3; in_sequence_id[1] = 2; in_source_chiplet_id[1] = 1;
            in_structural_dim[2] = 1; in_enterprise_type[2] = 0; in_sequence_id[2] = 9; in_source_chiplet_id[2] = 9;
            in_structural_dim[3] = 0; in_enterprise_type[3] = 3; in_sequence_id[3] = 1; in_source_chiplet_id[3] = 10;
            in_structural_dim[4] = 2; in_enterprise_type[4] = 0; in_sequence_id[4] = 1; in_source_chiplet_id[4] = 2;
            in_structural_dim[5] = 1; in_enterprise_type[5] = 0; in_sequence_id[5] = 8; in_source_chiplet_id[5] = 9;
            in_structural_dim[6] = 0; in_enterprise_type[6] = 3; in_sequence_id[6] = 1; in_source_chiplet_id[6] = 3;
            in_structural_dim[7] = 2; in_enterprise_type[7] = 0; in_sequence_id[7] = 1; in_source_chiplet_id[7] = 1;
            for (item = 0; item < COUNT; item = item + 1) begin
                in_payload_q32[item] = item * 64'sh0000000100000000;
                in_node_id[item] = item;
            end
            expected_id[0] = 6; expected_id[1] = 3; expected_id[2] = 1; expected_id[3] = 5;
            expected_id[4] = 2; expected_id[5] = 7; expected_id[6] = 4; expected_id[7] = 0;
        end
    endtask

    task automatic begin_snapshot;
        begin
            @(negedge clk);
            snapshot_begin = 1'b1;
            @(negedge clk);
            snapshot_begin = 1'b0;
        end
    endtask

    task automatic push_main_packet(input integer id);
        begin
            @(negedge clk);
            packet_valid = 1'b1;
            structural_dim = in_structural_dim[id];
            enterprise_type = in_enterprise_type[id];
            sequence_id = in_sequence_id[id];
            source_chiplet_id = in_source_chiplet_id[id];
            payload_q32 = in_payload_q32[id];
            node_id = in_node_id[id];
            @(negedge clk);
            packet_valid = 1'b0;
        end
    endtask

    task automatic close_snapshot;
        begin
            @(negedge clk);
            snapshot_close = 1'b1;
            @(negedge clk);
            snapshot_close = 1'b0;
        end
    endtask

    task automatic check_main_output(input string label, input integer trial_id);
        begin
            received = 0;
            while (!out_valid) @(negedge clk);
            while (out_valid) begin
                actual_id = expected_id[received];
                assert_true(out_structural_dim == in_structural_dim[actual_id], {label, " structural_dim"});
                assert_true(out_enterprise_type == in_enterprise_type[actual_id], {label, " enterprise_type"});
                assert_true(out_sequence_id == in_sequence_id[actual_id], {label, " sequence_id"});
                assert_true(out_source_chiplet_id == in_source_chiplet_id[actual_id], {label, " source_chiplet_id"});
                assert_true(out_payload_q32 == in_payload_q32[actual_id], {label, " payload"});
                assert_true(out_node_id == in_node_id[actual_id], {label, " node_id"});
                $display("RTL_SSC_TRACE case=%s trial=%0d index=%0d key=%0d,%0d,%0d,%0d node=%0d payload=%0d",
                    label, trial_id, received, out_structural_dim, out_enterprise_type,
                    out_sequence_id, out_source_chiplet_id, out_node_id, out_payload_q32);
                received = received + 1;
                @(negedge clk);
            end
            assert_true(received == COUNT, {label, " output_count"});
        end
    endtask

    task automatic run_affine_trial(input integer trial_id, input string case_label);
        integer affine_stride;
        integer affine_offset;
        begin
            // Four odd strides and eight offsets produce 32 distinct complete
            // arrival permutations. Each is repeated four times in the 128-run
            // campaign to test deterministic replay under identical inputs.
            affine_stride = ((trial_id % 4) * 2) + 1;
            affine_offset = trial_id % COUNT;
            begin_snapshot();
            for (item = 0; item < COUNT; item = item + 1)
                push_main_packet((item * affine_stride + affine_offset) % COUNT);
            close_snapshot();
            assert_true(!snapshot_rejected, "valid affine snapshot not rejected");
            check_main_output(case_label, trial_id);
        end
    endtask

    task automatic run_prefix_tie_case;
        begin
            begin_snapshot();
            @(negedge clk); packet_valid = 1; structural_dim = 4; enterprise_type = 2; sequence_id = 99; source_chiplet_id = 9; payload_q32 = 1; node_id = 4;
            @(negedge clk); structural_dim = 4; enterprise_type = 2; sequence_id = 99; source_chiplet_id = 3; payload_q32 = 1; node_id = 5;
            @(negedge clk); structural_dim = 4; enterprise_type = 2; sequence_id = 99; source_chiplet_id = 7; payload_q32 = 1; node_id = 6;
            @(negedge clk); packet_valid = 0;
            close_snapshot();
            while (!out_valid) @(negedge clk);
            assert_true(out_source_chiplet_id == 3, "prefix_tie first source"); @(negedge clk);
            assert_true(out_source_chiplet_id == 7, "prefix_tie second source"); @(negedge clk);
            assert_true(out_source_chiplet_id == 9, "prefix_tie third source"); @(negedge clk);
            assert_true(!out_valid, "prefix_tie output closed");
        end
    endtask

    task automatic run_exact_collision_case;
        begin
            begin_snapshot();
            @(negedge clk); packet_valid = 1; structural_dim = 3; enterprise_type = 4; sequence_id = 5; source_chiplet_id = 6; payload_q32 = 1; node_id = 10;
            @(negedge clk); structural_dim = 3; enterprise_type = 4; sequence_id = 5; source_chiplet_id = 6; payload_q32 = 2; node_id = 11;
            @(negedge clk); packet_valid = 0;
            @(negedge clk);
            assert_true(snapshot_rejected, "exact four-key collision rejected");
            close_snapshot();
            repeat (3) @(negedge clk);
            assert_true(!out_valid, "rejected snapshot has no ordered output");
        end
    endtask

    initial begin
        setup_main_vector();
        repeat (2) @(posedge clk);
        reset_n = 1'b1;
        for (trial = 0; trial < 128; trial = trial + 1)
            run_affine_trial(trial, "affine");
        $display("RTL_SSC_TEST affine_arrival_trials=128 unique_permutations=32 status=PASS");
        run_prefix_tie_case();
        $display("RTL_SSC_TEST prefix_tie_break status=PASS");
        run_exact_collision_case();
        $display("RTL_SSC_TEST exact_four_key_collision status=PASS");
        run_affine_trial(5, "recovery");
        $display("RTL_SSC_TEST recovery_after_reject status=PASS");
        if (failures == 0) begin
            $display("RTL_SSC_RESULT status=PASS");
            $finish(0);
        end
        $display("RTL_SSC_RESULT status=FAIL failures=%0d", failures);
        $fatal(1, "RTL SSC validation failed");
    end
endmodule
