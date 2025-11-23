import React, { useState, useEffect } from "react";
import { fetchAvailableBanks } from "../lib/api";

export default function TrendsForm({ onSubmit, loading }) {
  const [selectedBanks, setSelectedBanks] = useState(["Сбербанк"]);
  const [productType, setProductType] = useState("Кредитная карта");
  const [period, setPeriod] = useState("12m");
  const [availableBanks, setAvailableBanks] = useState([]);
  const [loadingBanks, setLoadingBanks] = useState(true);

  useEffect(() => {
    const loadBanks = async () => {
      try {
        const banks = await fetchAvailableBanks();
        setAvailableBanks(banks.all || []);
      } catch (error) {
        console.error("Failed to load banks:", error);
        setAvailableBanks([
          "Сбербанк",
          "ВТБ",
          "Альфа-Банк",
          "Т-Банк"
        ]);
      } finally {
        setLoadingBanks(false);
      }
    };
    loadBanks();
  }, []);

  const handleBankToggle = (bank) => {
    setSelectedBanks(prev => {
      if (prev.includes(bank)) {
        return prev.filter(b => b !== bank);
      } else {
        return [...prev, bank];
      }
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedBanks.length === 0) {
      alert("Выберите хотя бы один банк");
      return;
    }
    onSubmit({
      bank_names: selectedBanks,
      product_type: productType,
      period
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 rounded-3xl bg-slate-900/70 border border-slate-800/60 p-4 sm:p-5"
    >
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs text-slate-400">Режим</p>
          <p className="text-sm font-medium">Trends report</p>
        </div>
        <span className="text-[11px] text-slate-400">
          Multi-trends · {selectedBanks.length} банков
        </span>
      </div>

      <div className="space-y-3 text-xs">
        {/* Banks Multi-Select */}
        <div className="space-y-1.5">
          <label className="block text-slate-300">
            Банки для анализа ({selectedBanks.length} выбрано)
          </label>
          <div className="max-h-40 overflow-y-auto rounded-xl border border-slate-700 bg-slate-950/70 p-2 space-y-1">
            {loadingBanks ? (
              <p className="text-slate-400 text-center py-2">Загрузка...</p>
            ) : availableBanks.length === 0 ? (
              <p className="text-slate-400 text-center py-2">Нет доступных банков</p>
            ) : (
              availableBanks.map((bank) => (
                <label
                  key={bank}
                  className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-slate-800/50 cursor-pointer transition"
                >
                  <input
                    type="checkbox"
                    checked={selectedBanks.includes(bank)}
                    onChange={() => handleBankToggle(bank)}
                    className="w-3.5 h-3.5 rounded border-slate-600 text-brand-500 focus:ring-brand-400"
                  />
                  <span className="text-xs text-slate-200">{bank}</span>
                </label>
              ))
            )}
          </div>
        </div>

        {/* Product Type */}
        <div className="space-y-1.5">
          <label className="block text-slate-300">Тип продукта</label>
          <input
            value={productType}
            onChange={(e) => setProductType(e.target.value)}
            className="w-full rounded-xl border border-slate-700 bg-slate-950/70 px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-brand-400"
          />
        </div>

        {/* Period */}
        <div className="space-y-1.5">
          <label className="block text-slate-300">Период анализа</label>
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="w-full rounded-xl border border-slate-700 bg-slate-950/70 px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-brand-400"
          >
            <option value="6m">6 месяцев</option>
            <option value="12m">12 месяцев</option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={loading || loadingBanks || selectedBanks.length === 0}
        className="w-full inline-flex items-center justify-center rounded-xl bg-brand-500 hover:bg-brand-400 text-slate-950 text-xs font-semibold py-2.5 mt-2 transition disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {loading ? "Строим тренды..." : "Построить тренды"}
      </button>
      <p className="text-[11px] text-slate-500">
        Выберите несколько банков для сравнения трендов.
      </p>
    </form>
  );
}
