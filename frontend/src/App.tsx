import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RecipesPage from "./pages/Recipes";
import PlansPage from "./pages/Plans";
import NutritionPage from "./pages/Nutrition";
import NotFound from "./pages/NotFound";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { MealPlannerProvider } from "@/contexts/MealPlannerContext";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <MealPlannerProvider>
          <SidebarProvider>
            <div className="flex min-h-screen w-full">
              <AppSidebar />
              <SidebarInset>
                <header className="h-14 flex items-center border-b px-3 gap-2 sticky top-0 bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                  <SidebarTrigger />
                  <span className="font-semibold tracking-wide">NutriPlan</span>
                </header>
                <Routes>
                  <Route path="/" element={<Navigate to="/recipes" replace />} />
                  <Route path="/recipes" element={<RecipesPage />} />
                  <Route path="/plans" element={<PlansPage />} />
                  <Route path="/nutrition" element={<NutritionPage />} />
                  {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </SidebarInset>
            </div>
          </SidebarProvider>
        </MealPlannerProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
