import { Player } from "@/lib/mockData";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Eye, Star } from "lucide-react";

interface PlayerCardProps {
  player: Player;
  onClick: () => void;
  isMainSquad?: boolean;
}

export const PlayerCard = ({ player, onClick, isMainSquad = true }: PlayerCardProps) => {
  const getRoleBadgeVariant = (role: string) => {
    switch (role) {
      case "Batsman": return "default";
      case "Bowler": return "secondary";
      case "All-Rounder": return "outline";
      case "Wicket-Keeper": return "destructive";
      default: return "default";
    }
  };

  return (
    <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 cursor-pointer group">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-xl mb-2 group-hover:text-cyan-400 transition-colors text-white">
              {player.name}
            </CardTitle>
            <Badge variant={getRoleBadgeVariant(player.role)} className="text-xs">
              {player.role}
            </Badge>
          </div>
          {isMainSquad && (
            <Star className="h-5 w-5 text-accent fill-accent" />
          )}
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="bg-slate-700/40 backdrop-blur-sm p-3 rounded-lg border border-slate-600/30 hover:border-slate-500/50 transition-colors">
            <p className="text-slate-400 text-xs">Matches</p>
            <p className="font-bold text-lg text-cyan-400">{player.battingStats.matches}</p>
          </div>
          <div className="bg-slate-700/40 backdrop-blur-sm p-3 rounded-lg border border-slate-600/30 hover:border-slate-500/50 transition-colors">
            <p className="text-slate-400 text-xs">Runs</p>
            <p className="font-bold text-lg text-cyan-400">{player.battingStats.runs}</p>
          </div>
          <div className="bg-slate-700/40 backdrop-blur-sm p-3 rounded-lg border border-slate-600/30 hover:border-slate-500/50 transition-colors">
            <p className="text-slate-400 text-xs">Average</p>
            <p className="font-bold text-lg text-violet-400">{player.battingStats.average}</p>
          </div>
          <div className="bg-slate-700/40 backdrop-blur-sm p-3 rounded-lg border border-slate-600/30 hover:border-slate-500/50 transition-colors">
            <p className="text-slate-400 text-xs">SR</p>
            <p className="font-bold text-lg text-violet-400">{player.battingStats.strikeRate}</p>
          </div>
        </div>

        {player.bowlingStats && (
          <div className="pt-2 border-t border-slate-700/50">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Wickets:</span>
              <span className="font-semibold text-orange-400">{player.bowlingStats.wickets}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Economy:</span>
              <span className="font-semibold text-orange-400">{player.bowlingStats.economy}</span>
            </div>
          </div>
        )}
      </CardContent>

      <CardFooter>
        <Button 
          onClick={onClick} 
          className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
        >
          <Eye className="mr-2 h-4 w-4" />
          View Profile
        </Button>
      </CardFooter>
    </Card>
  );
};
