import React, { useState, useEffect } from "react";
import { fetchAvailableBanks } from "../lib/api";

const PRODUCT_TYPES = [
  "Кредитная карта",
  "Потребительский кредит",
  "Дебетовая карта",
  "Ипотека"
];

export default function UrgentForm({ onSubmit, loading }) {
  const [bankName, setBankName] = useState("Сбербанк");
  const [selectedCompetitors, setSelectedCompetitors] = useState(["ВТБ"]);
  const [productType, setProductType] = useState(PRODUCT_TYPES[0]);
  const [availableBanks, setAvailableBanks] = useState([]);
  const [loadingBanks, setLoadingBanks] = useState(true);

  useEffect(() => {
    const loadBanks = async () => {
      try {
        const banks = await fetchAvailableBanks();
        setAvailableBanks(banks.all || []);
      } catch (error) {
        console.error("Failed to load banks:", error);
        // Fallback to default list
        setAvailableBanks([
          "Сбербанк",
          "ВТБ",
          "Альфа-Банк",
          "Т-Банк",
          "Газпромбанк",
          "Локо-Банк",
          "МТС Банк",
          "Райффайзенбанк"
        ]);
      } finally {
        setLoadingBanks(false);
      }
    };
    loadBanks();
  }, []);

  const handleCompetitorToggle = (bank) => {
    setSelectedCompetitors(prev => {
      if (prev.includes(bank)) {
        return prev.filter(b => b !== bank);
      } else {
        return [...prev, bank];
      }
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedCompetitors.length === 0) {
      alert("Выберите хотя бы одного конкурента");
      return;
    }
    onSubmit({
      bank_name: bankName,
      competitor_names: selectedCompetitors,
      product_type: productType
    });
  };

  const competitorBanks = availableBanks.filter(bank => bank !== bankName);

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 rounded-3xl bg-slate-900/70 border border-slate-800/60 p-4 sm:p-5"
    >
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs text-slate-400">Режим</p>
          <p className="text-sm font-medium">Urgent report</p>
        </div>
        <span className="text-[11px] text-slate-400">
          Multi-banking · {selectedCompetitors.length} банков
        </span>
      </div>

      <div className="space-y-3 text-xs">
        {/* Base Bank Selection */}
        <div className="space-y-1.5">
          <label className="block text-slate-300">
            Базовый банк (эталон)
          </label>
          <select
            value={bankName}
            onChange={(e) => setBankName(e.target.value)}
            disabled={loadingBanks}
            className="w-full rounded-xl border border-slate-700 bg-slate-950/70 px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-brand-400"
          >
            {loadingBanks ? (
              <option>Загрузка...</option>
            ) : (
              availableBanks.map((bank) => (
                <option key={bank} value={bank}>
                  {bank}
                </option>
              ))
            )}
          </select>
        </div>

        {/* Competitor Multi-Select */}
        <div className="space-y-1.5">
          <label className="block text-slate-300">
            Конкуренты ({selectedCompetitors.length} выбрано)
          </label>
          <div className="max-h-40 overflow-y-auto rounded-xl border border-slate-700 bg-slate-950/70 p-2 space-y-1">
            {loadingBanks ? (
              <p className="text-slate-400 text-center py-2">Загрузка...</p>
            ) : competitorBanks.length === 0 ? (
              <p className="text-slate-400 text-center py-2">Нет доступных банков</p>
            ) : (
              competitorBanks.map((bank) => (
                <label
                  key={bank}
                  className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-slate-800/50 cursor-pointer transition"
                >
                  <input
                    type="checkbox"
                    checked={selectedCompetitors.includes(bank)}
                    onChange={() => handleCompetitorToggle(bank)}
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
          <select
            value={productType}
            onChange={(e) => setProductType(e.target.value)}
            className="w-full rounded-xl border border-slate-700 bg-slate-950/70 px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-brand-400"
          >
            {PRODUCT_TYPES.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={loading || loadingBanks || selectedCompetitors.length === 0}
        className="w-full inline-flex items-center justify-center rounded-xl bg-brand-500 hover:bg-brand-400 text-slate-950 text-xs font-semibold py-2.5 mt-2 transition disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {loading ? "Генерируем отчёт..." : "Сгенерировать отчёт"}
      </button>
      <p className="text-[11px] text-slate-500">
        Выберите несколько конкурентов для multi-bank сравнения.
      </p>
    </form>
  );
}
