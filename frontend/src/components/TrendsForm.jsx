import React, { useState, useEffect } from "react";
import { fetchAvailableBanks } from "../lib/api";

export default function TrendsForm({ onSubmit, loading }) {
  const [selectedBank, setSelectedBank] = useState("Сбербанк");
  const [productType, setProductType] = useState("Кредитная карта");
  const [period, setPeriod] = useState("12m");
  const [availableBanks, setAvailableBanks] = useState([]);
  const [loadingBanks, setLoadingBanks] = useState(true);

  useEffect(() => {
    const loadBanks = async () => {
      try {
        const banks = await fetchAvailableBanks();
        setAvailableBanks(banks.all || []);
        if (banks.all && banks.all.length > 0) {
          setSelectedBank(banks.all[0]);
        }
      } catch (error) {
        console.error("Failed to load banks:", error);
        setAvailableBanks([
          "Сбербанк",
          "ВТБ",
          "Альфа-Банк",
          "Т-Банк"
        ]);
        setSelectedBank("Сбербанк");
      } finally {
        setLoadingBanks(false);
      }
    };
    loadBanks();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedBank) {
      alert("Выберите один банк");
      return;
    }
    onSubmit({
      bank_names: [selectedBank],
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
        <span className="text-[11px] text-slate-400">Только 1 банк для трендов</span>
      </div>

      <div className="space-y-3 text-xs">
        {/* Single Bank Select */}
        <div className="space-y-1.5">
          <label className="block text-slate-300">
            Банк для трендов
          </label>
          <select
            value={selectedBank}
            onChange={(e) => setSelectedBank(e.target.value)}
            disabled={loadingBanks}
            className="w-full rounded-xl border border-slate-700 bg-slate-950/70 px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-brand-400"
          >
            {loadingBanks ? (
              <option>Загрузка...</option>
            ) : availableBanks.length === 0 ? (
              <option disabled>Нет доступных банков</option>
            ) : (
              availableBanks.map((bank) => (
                <option key={bank} value={bank}>{bank}</option>
              ))
            )}
          </select>
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
        disabled={loading || loadingBanks || !selectedBank}
        className="w-full inline-flex items-center justify-center rounded-xl bg-brand-500 hover:bg-brand-400 text-slate-950 text-xs font-semibold py-2.5 mt-2 transition disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {loading ? "Строим тренды..." : "Построить тренды"}
      </button>
      <p className="text-[11px] text-slate-500">Выберите один банк для трендового анализа.</p>
    </form>
  );
}
