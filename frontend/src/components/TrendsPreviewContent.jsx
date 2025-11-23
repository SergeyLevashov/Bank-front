import React from "react";

export default function TrendsPreviewContent({ data }) {
  // Use charts.trends only, and only draw when it exists
  const chartHtml = data.charts && (data.charts.trends || data.charts[Object.keys(data.charts)[0]]);

  // Summary should be an array of strings, never split by letters
  let summaryArr = [];
  if (Array.isArray(data.summary)) {
    summaryArr = data.summary.filter(x => typeof x === 'string');
  } else if (typeof data.summary === 'string') {
    summaryArr = [data.summary];
  }

  return (
    <div className="space-y-4">
      <div>
        <p className="text-[11px] text-slate-400">Банк и продукт</p>
        <p className="text-[13px] font-semibold">
          {(data.bank_names?.[0] || data.bank_name) + " · " + data.product_type + " (" + data.period + ")"}
        </p>
      </div>

      {/* HTML Chart */}
      {chartHtml && (
        <div className="my-2 rounded-xl border border-slate-800 overflow-hidden bg-white">
          <div dangerouslySetInnerHTML={{ __html: chartHtml }} className="w-full" />
        </div>
      )}

      {/* Summary */}
      {summaryArr.length > 0 && (
        <div>
          <p className="text-[11px] text-slate-400 mb-1.5">Резюме по тренду</p>
          <ul className="space-y-1.5">
            {summaryArr.map((item, idx) => (
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
