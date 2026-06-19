export type Status = "normal" | "low" | "high" | "info" | "flag";
export type ChartType = "bullet" | "status";

export interface Test {
  key: string;
  name: string;
  section: string;
  value: number | null;
  value_text: string;
  unit: string;
  ref_text: string;
  status: Status;
  note: string;
  axis_min: number;
  axis_max: number;
  band_low: number | null;
  band_high: number | null;
}

export interface Patient {
  name: string;
  first_name: string;
  age: number;
  gender: string;
  lab_no: string;
  collected: string;
  reported: string;
  headline: string;
  flagged_count: number;
  total_count: number;
  section_summary: Record<string, string>;
  tests: Test[];
}

export interface Section {
  key: string;
  title: string;
  icon: string;
  story: string;
  area: string;
  chart_type: ChartType;
  order: number;
}

export interface ReportDoc {
  sections: Section[];
  patients: Patient[];
}
