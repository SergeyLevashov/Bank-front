import React from "react";

export default function TrendsPreviewContent({ data }) {
  const chartHtml = data.charts && data.charts.trends;

  return (
    <div className="space-y-4">
      <div>
        <p className="text-[11px] text-slate-400">Банк и продукт</p>
        <p className="text-[13px] font-semibold">
          {(data.bank_names?.[0] || data.bank_name) + " · " + data.product_type + " (" + data.period + ")"}
        </p>
      </div>

      {/* Plotly Chart (dynamic) */}
      {chartHtml && (
        <div className="my-2 rounded-xl border border-slate-800 overflow-hidden bg-white">
          <div dangerouslySetInnerHTML={{ __html: chartHtml }} className="w-full" />
        </div>
      )}

      {/* Summary & Resume */}
      {data.summary?.length > 0 && (
        <div>
          <p className="text-[11px] text-slate-400 mb-1.5">Резюме по тренду</p>
          <ul className="space-y-1.5">
            {data.summary.map((item, idx) => (
              <li key={idx} className="flex gap-2">
                <span className="mt-1 h-1 w-1 rounded-full bg-sky-400" />
                <p className="text-[11px] text-slate-200">{item}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}