import { readFileSync } from "node:fs";

const sourcePath = process.argv[2] ?? "evidence/native-reference/cherry-scale-load1-20260822/inner/scaling-load.json";
const report = JSON.parse(readFileSync(sourcePath, "utf8"));

const round = (value) => Number(value.toFixed(3));

function endpointRows(kind, label, xField, rateField) {
  const points = report.points.filter((point) => point.kind === kind);
  const first = points[0];
  const last = points.at(-1);
  const metrics = ["t_agg_us", "t_fuse_us", "t_ssc_us", "t_total_us"];

  return metrics.map((metric) => {
    const start = first.timing_mean_us[metric];
    const end = last.timing_mean_us[metric];
    return {
      series: label,
      metric,
      start_condition: first[xField],
      end_condition: last[xField],
      start_mean_us: start,
      end_mean_us: end,
      delta_mean_us: round(end - start),
      percent_change: round(((end - start) / start) * 100),
    };
  }).concat([
    {
      series: label,
      metric: rateField,
      start_condition: first[xField],
      end_condition: last[xField],
      start_value: first[rateField],
      end_value: last[rateField],
      delta_value: round(last[rateField] - first[rateField]),
      percent_change: round(((last[rateField] - first[rateField]) / first[rateField]) * 100),
    },
  ]);
}

const result = {
  source_domain: report.domain,
  source_limitation: report.limitation,
  scaling_endpoints: endpointRows("scaling", "SCL-01", "logical_nodes", "events_per_second"),
  load_endpoints: endpointRows("load", "LOD-01", "target_input_events_per_second", "observed_reference_events_per_second"),
  jitter_available: false,
  jitter_reason: "The retained JSON stores timing means per point, not per-epoch timing samples or a distribution.",
};

console.log(JSON.stringify(result, null, 2));
