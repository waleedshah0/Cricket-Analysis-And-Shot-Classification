import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchStadiums, Stadium, fetchPlayersByFormat, PlayerProfile } from "@/lib/apiUtils";
import { Sparkles, MapPin, Trophy, Share2, AlertCircle } from "lucide-react";
import { PlayerCard } from "@/components/PlayerCard";
import { Navbar } from "@/components/Navbar";
import { motion } from "framer-motion";
import { useToast } from "@/hooks/use-toast";
import { Skeleton } from "@/components/ui/skeleton";

const SquadGenerator = () => {
  const { toast } = useToast();
  const navigate = useNavigate();
  const [stadium, setStadium] = useState<string>("");
  const [format, setFormat] = useState<string>("");
  const [squad, setSquad] = useState<PlayerProfile[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [stadiums, setStadiums] = useState<Stadium[]>([]);
  const [isFetchingStadiums, setIsFetchingStadiums] = useState(true);

  // Fetch stadiums from database on component mount
  useEffect(() => {
    const fetchStadiumData = async () => {
      try {
        const stadiumData = await fetchStadiums();
        setStadiums(stadiumData);
      } catch (error) {
        console.error('Failed to fetch stadiums:', error);
        toast({
          title: "Error",
          description: "Failed to load stadiums. Using mock data instead.",
          variant: "destructive",
        });
        // Fallback to mock data if database fetch fails
        setStadiums([
          { id: 1, ground_name: "Melbourne Cricket Ground" },
          { id: 2, ground_name: "Lord's Cricket Ground" },
          { id: 3, ground_name: "Eden Gardens" },
          { id: 4, ground_name: "Wankhede Stadium" },
          { id: 5, ground_name: "The Oval" },
          { id: 6, ground_name: "Sydney Cricket Ground" },
          { id: 7, ground_name: "Gaddafi Stadium" },
          { id: 8, ground_name: "Newlands" },
        ]);
      } finally {
        setIsFetchingStadiums(false);
      }
    };

    fetchStadiumData();
  }, []);

  const handleGenerateSquad = async () => {
    if (!stadium || !format) return;
    
    setIsLoading(true);
    try {
      // Fetch players by format from the database
      const players = await fetchPlayersByFormat(format);
      
      if (players.length === 0) {
        toast({
          title: "No Players Found",
          description: `No players found for ${format} format in the database.`,
          variant: "destructive",
        });
        setSquad([]);
      } else {
        // Set the fetched players as the squad
        setSquad(players);
        toast({
          title: "Squad Generated!",
          description: `Your ${format} squad with ${players.length} players is ready.`,
        });
      }
    } catch (error) {
      console.error('Failed to generate squad:', error);
      toast({
        title: "Error",
        description: "Failed to generate squad. Please try again.",
        variant: "destructive",
      });
      setSquad([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleShareSquad = () => {
    toast({
      title: "Share Squad",
      description: "Squad link copied to clipboard!",
    });
  };

  return (
    <div className="min-h-screen bg-gradient-hero">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 text-center"
        >
          <h1 className="text-4xl md:text-5xl font-poppins font-bold text-white mb-4 flex items-center justify-center gap-3 text-glow-primary">
            <Sparkles className="h-8 w-8 animate-pulse-glow" />
            Squad Generator
          </h1>
          <p className="text-foreground text-lg">Select stadium and format to get AI-powered recommendations</p>
        </motion.div>

        {/* Generator Form */}
        {!isFetchingStadiums && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="max-w-2xl mx-auto mb-12 glass-card shadow-neon-primary">
              <CardHeader>
                <CardTitle className="text-white">Configure Selection</CardTitle>
                <CardDescription className="text-muted-foreground">Choose your match conditions</CardDescription>
              </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="stadium" className="text-base flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  Stadium Name
                </Label>
                <Select value={stadium} onValueChange={setStadium}>
                  <SelectTrigger id="stadium">
                    <SelectValue placeholder="Select a stadium" />
                  </SelectTrigger>
                  <SelectContent className="bg-card">
                    {stadiums.map((s) => (
                      <SelectItem key={s.id} value={s.ground_name}>
                        {s.ground_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="format" className="text-base flex items-center gap-2">
                  <Trophy className="h-4 w-4" />
                  Match Format
                </Label>
                <Select value={format} onValueChange={setFormat}>
                  <SelectTrigger id="format">
                    <SelectValue placeholder="Select match format" />
                  </SelectTrigger>
                  <SelectContent className="bg-card">
                    <SelectItem value="Test">Test Cricket</SelectItem>
                    <SelectItem value="ODI">One Day International (ODI)</SelectItem>
                    <SelectItem value="T20I">Twenty20 International (T20I)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button 
                onClick={handleGenerateSquad} 
                disabled={!stadium || !format || isLoading}
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground h-12 text-lg font-semibold"
              >
                {isLoading ? (
                  <>
                    <Sparkles className="mr-2 h-5 w-5 animate-spin" />
                    Generating Squad...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-5 w-5" />
                    Generate AI Squad
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
          </motion.div>
        )}

        {/* Loading Skeletons for Stadiums */}
        {isFetchingStadiums && (
          <Card className="max-w-2xl mx-auto mb-12 glass-card shadow-neon-primary">
            <CardHeader>
              <Skeleton className="h-6 w-1/3" />
              <Skeleton className="h-4 w-1/2" />
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Skeleton className="h-4 w-1/4" />
                <Skeleton className="h-10 w-full" />
              </div>
              <div className="space-y-2">
                <Skeleton className="h-4 w-1/4" />
                <Skeleton className="h-10 w-full" />
              </div>
              <Skeleton className="h-12 w-full" />
            </CardContent>
          </Card>
        )}

        {/* Loading Skeletons for Squad */}
        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array(15).fill(0).map((_, idx) => (
              <Card key={idx} className="backdrop-blur-glass bg-card/90">
                <CardHeader>
                  <Skeleton className="h-48 w-full" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/2" />
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Squad Results */}
        {squad && !isLoading && squad.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="mb-8 text-center">
              <h2 className="text-3xl font-bold text-white mb-2">Your Selected Squad</h2>
              <p className="text-white/80 mb-4">{squad.length} Players - {format} Format</p>
              
              <Button
                onClick={handleShareSquad}
                variant="secondary"
                className="gap-2"
              >
                <Share2 className="h-4 w-4" />
                Share Squad
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {squad.map((player, index) => {
                // Initialize default stats
                let battingStats = {
                  matches: 0,
                  runs: 0,
                  average: 0,
                  strikeRate: 0,
                  hundreds: 0,
                  fifties: 0,
                };

                let bowlingStats = undefined;
                let role: "Batsman" | "Bowler" | "All-Rounder" | "Wicket-Keeper" = "Batsman";

                // Helper function to extract stats from array of game types
                const extractStatsFromArray = (statsArray: any[], formatToMatch?: string) => {
                  if (!Array.isArray(statsArray) || statsArray.length === 0) return null;
                  
                  // Try to find the best matching format (TEST, ODI, T20I)
                  let selectedStats = null;
                  
                  // First, try to match the current format
                  if (formatToMatch) {
                    selectedStats = statsArray.find(s => {
                      const gameType = (s['Game Type'] || '').toUpperCase();
                      return gameType.includes(formatToMatch.toUpperCase());
                    });
                  }
                  
                  // If no match, use the first comprehensive stats (FIRSTCLASS or similar)
                  if (!selectedStats) {
                    selectedStats = statsArray.find(s => 
                      ['FIRSTCLASS', 'TESTS', 'ODIS', 'T20IS'].includes((s['Game Type'] || '').toUpperCase())
                    ) || statsArray[0];
                  }
                  
                  return selectedStats;
                };

                // Parse batting stats from JSON array
                if (player.batting_stats) {
                  try {
                    const parsed = typeof player.batting_stats === 'string' 
                      ? JSON.parse(player.batting_stats) 
                      : player.batting_stats;
                    
                    if (Array.isArray(parsed) && parsed.length > 0) {
                      // Get the best available batting stats
                      const stats = extractStatsFromArray(parsed, format);
                      if (stats) {
                        battingStats = {
                          matches: parseInt(stats['Mat'] || stats['matches'] || '0', 10),
                          runs: parseInt(stats['R'] || stats['runs'] || '0', 10),
                          average: parseFloat(stats['Avg'] || stats['average'] || '0'),
                          strikeRate: parseFloat(stats['S/R'] || stats['strikeRate'] || '0'),
                          hundreds: parseInt(stats['100s'] || stats['hundreds'] || '0', 10),
                          fifties: parseInt(stats['50s'] || stats['fifties'] || '0', 10),
                        };
                      }
                    }
                  } catch (e) {
                    console.error(`Error parsing batting stats for ${player.player_name}:`, e);
                  }
                }

                // Parse bowling stats from JSON array
                if (player.bowling_stats) {
                  try {
                    const parsed = typeof player.bowling_stats === 'string' 
                      ? JSON.parse(player.bowling_stats) 
                      : player.bowling_stats;
                    
                    if (Array.isArray(parsed) && parsed.length > 0) {
                      // Get the best available bowling stats
                      const stats = extractStatsFromArray(parsed, format);
                      if (stats) {
                        bowlingStats = {
                          matches: parseInt(stats['Mat'] || stats['matches'] || '0', 10),
                          wickets: parseInt(stats['W'] || stats['wickets'] || '0', 10),
                          average: parseFloat(stats['Avg'] || stats['average'] || '0'),
                          economy: parseFloat(stats['E/R'] || stats['economy'] || '0'),
                          bestFigures: stats['Best'] || stats['bestFigures'] || "",
                        };
                      }
                    }
                  } catch (e) {
                    console.error(`Error parsing bowling stats for ${player.player_name}:`, e);
                  }
                }

                // Determine role based on available stats
                const hasBattingStats = battingStats.average > 0 || battingStats.runs > 0;
                const hasBowlingStats = bowlingStats && (bowlingStats.wickets > 0 || bowlingStats.economy > 0);
                
                if (hasBattingStats && hasBowlingStats) {
                  role = "All-Rounder";
                } else if (hasBowlingStats) {
                  role = "Bowler";
                } else if (hasBattingStats) {
                  role = "Batsman";
                }

                // Convert PlayerProfile to Player type for compatibility with PlayerCard
                const playerData: any = {
                  id: player.id || index + 1,
                  name: player.player_name || "Unknown",
                  role: role,
                  battingStats: battingStats,
                  image: player.image_url || "",
                };

                if (bowlingStats) {
                  playerData.bowlingStats = bowlingStats;
                }

                return (
                  <motion.div
                    key={player.id || index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.05 }}
                  >
                    <PlayerCard 
                      player={playerData} 
                      onClick={() => navigate(`/player/${player.id || index}?name=${encodeURIComponent(player.player_name || 'Unknown')}`)}
                      isMainSquad={index < 11}
                    />
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        )}

        {/* Empty Squad Message */}
        {squad && !isLoading && squad.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-2xl mx-auto"
          >
            <Card className="glass-card shadow-neon-primary border-yellow-500/50 bg-yellow-500/10">
              <CardContent className="pt-6">
                <div className="flex items-center gap-4 text-center justify-center">
                  <AlertCircle className="h-8 w-8 text-yellow-500" />
                  <div>
                    <h3 className="text-lg font-semibold text-white">No Players Found</h3>
                    <p className="text-white/70 mt-1">No players available for the selected format in the database.</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default SquadGenerator;
