import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { Recipe } from "@/data/recipes";

type MealSlots = "breakfast" | "lunch" | "dinner";
export type DayPlan = Partial<Record<MealSlots, string>>; // recipe id by slot
export type Plans = Record<string, DayPlan>; // key: YYYY-MM-DD

type MealPlannerContextType = {
  saved: Set<string>;
  toggleSave: (id: string) => void;
  plans: Plans;
  setMeal: (dateKey: string, slot: MealSlots, recipeId: string | undefined) => void;
  clearDays: (dateKeys: string[]) => void;
};

const MealPlannerContext = createContext<MealPlannerContextType | null>(null);

const SAVED_KEY = "nutriplan:saved";
const PLANS_KEY = "nutriplan:plans";

export const MealPlannerProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [saved, setSaved] = useState<Set<string>>(new Set());
  const [plans, setPlans] = useState<Plans>({});

  useEffect(() => {
    try {
      const s = JSON.parse(localStorage.getItem(SAVED_KEY) || "[]") as string[];
      setSaved(new Set(s));
      const p = JSON.parse(localStorage.getItem(PLANS_KEY) || "{}") as Plans;
      setPlans(p);
    } catch {}
  }, []);

  useEffect(() => {
    localStorage.setItem(SAVED_KEY, JSON.stringify(Array.from(saved)));
  }, [saved]);

  useEffect(() => {
    localStorage.setItem(PLANS_KEY, JSON.stringify(plans));
  }, [plans]);

  const toggleSave = (id: string) => {
    setSaved((prev) => {
      const n = new Set(prev);
      if (n.has(id)) n.delete(id); else n.add(id);
      return n;
    });
  };

  const setMeal = (dateKey: string, slot: MealSlots, recipeId: string | undefined) => {
    setPlans((prev) => {
      const day = { ...(prev[dateKey] || {}) } as DayPlan;
      if (!recipeId) delete day[slot]; else day[slot] = recipeId;
      return { ...prev, [dateKey]: day };
    });
  };

  const clearDays = (dateKeys: string[]) => {
    setPlans((prev) => {
      const next = { ...prev } as Plans;
      for (const k of dateKeys) delete next[k];
      return next;
    });
  };

  const value = useMemo(() => ({ saved, toggleSave, plans, setMeal, clearDays }), [saved, plans]);

  return <MealPlannerContext.Provider value={value}>{children}</MealPlannerContext.Provider>;
};

export const useMealPlanner = () => {
  const ctx = useContext(MealPlannerContext);
  if (!ctx) throw new Error("useMealPlanner must be used within MealPlannerProvider");
  return ctx;
};
