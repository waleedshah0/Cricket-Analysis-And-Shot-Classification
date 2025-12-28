import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { MOCK_PLAYERS } from "@/lib/mockData";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft, TrendingUp, AlertCircle } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Navbar } from "@/components/Navbar";
import { motion } from "framer-motion";
import { fetchPlayerProfile, PlayerProfile } from "@/lib/apiUtils";
import { Skeleton } from "@/components/ui/skeleton";

const PlayerDetails = () => {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [playerData, setPlayerData] = useState<PlayerProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Get player name from query parameter
  const queryParams = new URLSearchParams(location.search);
  const playerNameFromUrl = queryParams.get('name');
  
  // Fallback to mock data if available
  const mockPlayer = MOCK_PLAYERS.find((p) => p.id === Number(id));

  useEffect(() => {
    const loadPlayerProfile = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // Use player name from URL parameter first, then fallback to mock player name
        const playerName = playerNameFromUrl || mockPlayer?.name;
        
        console.log('Loading profile for player:', playerName);
        
        if (playerName) {
          const profile = await fetchPlayerProfile(playerName);
          console.log('Profile data received:', profile);
          if (profile) {
            setPlayerData(profile);
          } else {
            console.log('No profile found for player:', playerName);
            setError(`No profile found for ${playerName}`);
          }
        } else {
          setError('Player name not found');
        }
      } catch (err) {
        console.error('Error fetching player profile:', err);
        setError('Failed to load player profile');
      } finally {
        setIsLoading(false);
      }
    };

    loadPlayerProfile();
  }, [id, playerNameFromUrl, mockPlayer?.name]);

  // Helper function to extract stats from array
  const extractStats = (statsArray: any, statType: 'batting' | 'bowling') => {
    if (!Array.isArray(statsArray) || statsArray.length === 0) return null;
    
    // Get the first comprehensive stat entry (FIRSTCLASS, TEST, etc.)
    const selected = statsArray.find((s: any) => {
      const gameType = (s['Game Type'] || '').toUpperCase();
      return ['FIRSTCLASS', 'TESTS', 'ODIS', 'T20IS'].includes(gameType);
    }) || statsArray[0];
    
    if (statType === 'batting') {
      return {
        matches: parseInt(selected['Mat'] || '0', 10),
        runs: parseInt(selected['R'] || '0', 10),
        average: parseFloat(selected['Avg'] || '0'),
        strikeRate: parseFloat(selected['S/R'] || '0'),
        hundreds: parseInt(selected['100s'] || '0', 10),
        fifties: parseInt(selected['50s'] || '0', 10),
        gameType: selected['Game Type'] || '',
      };
    } else {
      return {
        matches: parseInt(selected['Mat'] || '0', 10),
        wickets: parseInt(selected['W'] || '0', 10),
        average: parseFloat(selected['Avg'] || '0'),
        economy: parseFloat(selected['E/R'] || '0'),
        bestFigures: selected['Best'] || '',
        gameType: selected['Game Type'] || '',
      };
    }
  };

  // Parse stats if available
  let battingStats = null;
  let bowlingStats = null;
  
  if (playerData) {
    console.log('Parsing stats for playerData:', playerData);
    if (playerData.batting_stats) {
      try {
        const statsArray = typeof playerData.batting_stats === 'string' 
          ? JSON.parse(playerData.batting_stats) 
          : playerData.batting_stats;
        battingStats = extractStats(statsArray, 'batting');
        console.log('Extracted batting stats:', battingStats);
      } catch (e) {
        console.error('Error parsing batting stats:', e);
      }
    }
    
    if (playerData.bowling_stats) {
      try {
        const statsArray = typeof playerData.bowling_stats === 'string' 
          ? JSON.parse(playerData.bowling_stats) 
          : playerData.bowling_stats;
        bowlingStats = extractStats(statsArray, 'bowling');
        console.log('Extracted bowling stats:', bowlingStats);
      } catch (e) {
        console.error('Error parsing bowling stats:', e);
      }
    }
  }

  if (!mockPlayer && !playerData) {
    return (
      <div className="min-h-screen bg-gradient-hero flex items-center justify-center">
        <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50">
          <CardHeader>
            <CardTitle className="text-white">Player not found</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-400 mb-4">The player could not be found in our database.</p>
            <Button onClick={() => navigate("/generator")} className="bg-cyan-600 hover:bg-cyan-700">Back to Generator</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Check if profile data failed to load
  const profileNotFound = !isLoading && error && !playerData;

  const getRoleBadgeVariant = (role: string) => {
    switch (role) {
      case "Batsman": return "default";
      case "Bowler": return "secondary";
      case "All-Rounder": return "outline";
      case "Wicket-Keeper": return "destructive";
      default: return "default";
    }
  };

  const displayName = playerData?.player_name || playerNameFromUrl || mockPlayer?.name || 'Unknown';
  const displayImage = playerData?.image_url || mockPlayer?.image || '/placeholder.png';

  return (
    <div className="min-h-screen bg-gradient-hero">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <Button 
            variant="outline" 
            onClick={() => navigate("/generator")}
            className="mb-6 bg-card/90 backdrop-blur-sm hover:bg-card border-border"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Squad
          </Button>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Player Profile Card */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-1"
          >
            <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-2xl sticky top-24">
              <CardHeader className="text-center">
                <div className="mx-auto mb-4 w-32 h-32 rounded-full overflow-hidden border-4 border-cyan-400">
                  <img 
                    src={displayImage} 
                    alt={displayName}
                    className="w-full h-full object-cover"
                  />
                </div>
                <CardTitle className="text-2xl text-white">{displayName}</CardTitle>
                <div className="flex justify-center gap-2 mt-2">
                  {mockPlayer && <Badge variant={getRoleBadgeVariant(mockPlayer.role)}>{mockPlayer.role}</Badge>}
                  {!mockPlayer && playerData && <Badge variant="default">Database Player</Badge>}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {isLoading && (
                  <>
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                  </>
                )}
                {profileNotFound && (
                  <div className="text-sm text-orange-400 flex items-start gap-2 p-3 bg-orange-500/10 rounded-lg border border-orange-500/20">
                    <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
                    <p>Player profile not in database. Basic info shown only.</p>
                  </div>
                )}
                {playerData?.personal_info && (
                  <>
                    {playerData.personal_info['Full Name'] && (
                      <div>
                        <p className="text-sm text-slate-400">Full Name</p>
                        <p className="font-semibold text-white">{playerData.personal_info['Full Name']}</p>
                      </div>
                    )}
                    {playerData.personal_info['Age'] && (
                      <div>
                        <p className="text-sm text-slate-400">Age</p>
                        <p className="font-semibold text-white">{playerData.personal_info['Age']}</p>
                      </div>
                    )}
                    {playerData.personal_info['Nationality'] && (
                      <div>
                        <p className="text-sm text-slate-400">Nationality</p>
                        <p className="font-semibold text-white">{playerData.personal_info['Nationality']}</p>
                      </div>
                    )}
                    {playerData.personal_info['Playing Role'] && (
                      <div>
                        <p className="text-sm text-slate-400">Playing Role</p>
                        <p className="font-semibold text-white">{playerData.personal_info['Playing Role']}</p>
                      </div>
                    )}
                    {playerData.personal_info['Batting Style'] && (
                      <div>
                        <p className="text-sm text-slate-400">Batting Style</p>
                        <p className="font-semibold text-white">{playerData.personal_info['Batting Style']}</p>
                      </div>
                    )}
                    {playerData.personal_info['Bowling Style'] && (
                      <div>
                        <p className="text-sm text-slate-400">Bowling Style</p>
                        <p className="font-semibold text-white">{playerData.personal_info['Bowling Style']}</p>
                      </div>
                    )}
                  </>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Stats Section or Error Message */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            {isLoading ? (
              <div className="space-y-6">
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-96 w-full" />
              </div>
            ) : (battingStats || bowlingStats) ? (
              <Tabs defaultValue="overview" className="space-y-6">
                <TabsList className="grid w-full grid-cols-3 bg-slate-800 border border-slate-700">
                  <TabsTrigger value="overview" className="text-white data-[state=active]:bg-cyan-600">Overview</TabsTrigger>
                  <TabsTrigger value="batting" className="text-white data-[state=active]:bg-cyan-600">Batting</TabsTrigger>
                  {bowlingStats && <TabsTrigger value="bowling" className="text-white data-[state=active]:bg-cyan-600">Bowling</TabsTrigger>}
                </TabsList>
                <TabsContent value="overview" className="space-y-6">
                  {battingStats && bowlingStats ? (
                    <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl">
                      <CardHeader>
                        <CardTitle className="text-white">Format: {battingStats.gameType}</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                          <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                            <p className="text-3xl font-bold text-cyan-400">{battingStats.matches}</p>
                            <p className="text-sm text-slate-400">Matches</p>
                          </div>
                          <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                            <p className="text-3xl font-bold text-cyan-400">{battingStats.runs}</p>
                            <p className="text-sm text-slate-400">Runs</p>
                          </div>
                          <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                            <p className="text-3xl font-bold text-violet-400">{battingStats.average}</p>
                            <p className="text-sm text-slate-400">Batting Avg</p>
                          </div>
                          <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                            <p className="text-3xl font-bold text-violet-400">{battingStats.strikeRate}</p>
                            <p className="text-sm text-slate-400">Strike Rate</p>
                          </div>
                          <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                            <p className="text-3xl font-bold text-orange-400">{bowlingStats.wickets}</p>
                            <p className="text-sm text-slate-400">Wickets</p>
                          </div>
                          <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                            <p className="text-3xl font-bold text-orange-400">{bowlingStats.economy}</p>
                            <p className="text-sm text-slate-400">Economy</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ) : (
                    <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl">
                      <CardContent className="py-12 text-center">
                        <p className="text-slate-400">Stats not available</p>
                      </CardContent>
                    </Card>
                  )}
                </TabsContent>

                <TabsContent value="batting" className="space-y-6">
                  {battingStats ? (
                    <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-white">
                      <TrendingUp className="h-5 w-5" />
                      Batting Statistics ({battingStats.gameType})
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-cyan-400">{battingStats.matches}</p>
                        <p className="text-sm text-slate-400">Matches</p>
                      </div>
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-cyan-400">{battingStats.runs}</p>
                        <p className="text-sm text-slate-400">Runs</p>
                      </div>
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-violet-400">{battingStats.average.toFixed(2)}</p>
                        <p className="text-sm text-slate-400">Average</p>
                      </div>
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-violet-400">{battingStats.strikeRate.toFixed(2)}</p>
                        <p className="text-sm text-slate-400">Strike Rate</p>
                      </div>
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-yellow-400">{battingStats.hundreds}</p>
                        <p className="text-sm text-slate-400">Centuries</p>
                      </div>
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-yellow-400">{battingStats.fifties}</p>
                        <p className="text-sm text-slate-400">Half Centuries</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                  ) : (
                    <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl">
                      <CardContent className="py-12 text-center">
                        <p className="text-slate-400">No batting statistics available</p>
                      </CardContent>
                    </Card>
                  )}
                </TabsContent>

                <TabsContent value="bowling" className="space-y-6">
                  {bowlingStats ? (
                    <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-white">
                      <TrendingUp className="h-5 w-5" />
                      Bowling Statistics ({bowlingStats.gameType})
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-orange-400">{bowlingStats.wickets}</p>
                        <p className="text-sm text-slate-400">Wickets</p>
                      </div>
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-orange-400">{bowlingStats.average.toFixed(2)}</p>
                        <p className="text-sm text-slate-400">Average</p>
                      </div>
                      <div className="text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-cyan-400">{bowlingStats.economy.toFixed(2)}</p>
                        <p className="text-sm text-slate-400">Economy</p>
                      </div>
                      <div className="col-span-2 md:col-span-3 text-center p-4 bg-slate-700/40 rounded-lg border border-slate-600/30">
                        <p className="text-3xl font-bold text-emerald-400">{bowlingStats.bestFigures}</p>
                        <p className="text-sm text-slate-400">Best Figures</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                  ) : (
                    <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl">
                      <CardContent className="py-12 text-center">
                        <p className="text-slate-400">No bowling statistics available</p>
                      </CardContent>
                    </Card>
                  )}
                </TabsContent>
              </Tabs>
            ) : (
              <Card className="backdrop-blur-glass bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 shadow-xl">
                <CardContent className="py-12">
                  <div className="text-center space-y-4">
                    <div className="flex items-center justify-center gap-3 text-orange-400 mb-4">
                      <AlertCircle className="h-8 w-8" />
                      <p className="text-lg font-semibold">Profile Data Not Found</p>
                    </div>
                    <p className="text-slate-400">The detailed profile for <strong>{displayName}</strong> is not available in our database yet.</p>
                    <p className="text-slate-500 text-sm">We have 52 players in our squad database, but only 34 have complete profile data. This player may not have been scraped yet.</p>
                    <div className="pt-4">
                      <Button 
                        onClick={() => navigate("/generator")}
                        className="bg-cyan-600 hover:bg-cyan-700"
                      >
                        Back to Squad Generator
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default PlayerDetails;
