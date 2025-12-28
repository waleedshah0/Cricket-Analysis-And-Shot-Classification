import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import SquadGenerator from "./pages/SquadGenerator";
import PlayerDetails from "./pages/PlayerDetails";
import BattingAnalysis from "./pages/BattingAnalysis";
import BowlingAnalysis from "./pages/BowlingAnalysis";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/generator" element={<SquadGenerator />} />
          <Route path="/player/:id" element={<PlayerDetails />} />
          <Route path="/analyze-batting" element={<BattingAnalysis />} />
          <Route path="/analyze-bowling" element={<BowlingAnalysis />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
