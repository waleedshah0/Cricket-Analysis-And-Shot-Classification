import { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Upload, PlayCircle, TrendingUp, Activity, Zap } from "lucide-react";
import { motion } from "framer-motion";
import { useToast } from "@/hooks/use-toast";

interface BowlingAnalysisResult {
  runUpAnalysis: number;
  releasePoint: string;
  armAngle: number;
  followThrough: number;
  bowlingType: string;
  lineAndLength: { good: number; short: number; full: number };
  speedEstimation: string;
  keyFrames: string[];
  recommendations: string[];
}

const BowlingAnalysis = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<BowlingAnalysisResult | null>(null);
  const { toast } = useToast();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const validTypes = ["video/mp4", "video/quicktime", "video/x-msvideo"];
      if (!validTypes.includes(file.type)) {
        toast({
          title: "Invalid file type",
          description: "Please upload a .mp4, .mov, or .avi file",
          variant: "destructive",
        });
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setUploadProgress(0);

    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 200);

    setTimeout(() => {
      clearInterval(progressInterval);
      setUploadProgress(100);

      setAnalysisResult({
        runUpAnalysis: 88,
        releasePoint: "Optimal",
        armAngle: 142,
        followThrough: 82,
        bowlingType: "Fast-Medium Pace",
        lineAndLength: { good: 72, short: 15, full: 13 },
        speedEstimation: "135-140 km/h",
        keyFrames: Array(6).fill("/placeholder.svg"),
        recommendations: [
          "Maintain consistent run-up rhythm",
          "Release point is excellent - keep this consistency",
          "Work on yorker execution for better length variation",
          "Follow-through could be extended for more pace",
        ],
      });

      setIsAnalyzing(false);
      toast({
        title: "Analysis Complete!",
        description: "Your bowling performance has been analyzed",
      });
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            AI Bowling Performance Analyzer
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Upload your bowling footage. AI analyzes run-up, release point, arm angle & line-length.
          </p>
        </motion.div>

        {!analysisResult ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="max-w-2xl mx-auto backdrop-blur-glass bg-card/90 border-border/50 shadow-2xl">
              <CardHeader>
                <CardTitle>Upload Bowling Video</CardTitle>
                <CardDescription>Support: .mp4, .mov, .avi (Max 100MB)</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="border-2 border-dashed border-border/50 rounded-lg p-12 text-center hover:border-primary/50 transition-colors cursor-pointer bg-gradient-card">
                  <input
                    type="file"
                    id="video-upload"
                    className="hidden"
                    accept=".mp4,.mov,.avi"
                    onChange={handleFileSelect}
                  />
                  <label htmlFor="video-upload" className="cursor-pointer">
                    <Upload className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                    <p className="text-lg font-semibold mb-2">
                      {selectedFile ? selectedFile.name : "Click to upload or drag and drop"}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Video files up to 100MB
                    </p>
                  </label>
                </div>

                {selectedFile && (
                  <div className="space-y-4">
                    {isAnalyzing && (
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Analyzing video...</span>
                          <span>{uploadProgress}%</span>
                        </div>
                        <Progress value={uploadProgress} />
                      </div>
                    )}

                    <Button
                      onClick={handleAnalyze}
                      disabled={isAnalyzing}
                      className="w-full h-12 text-lg bg-primary hover:bg-primary/90"
                    >
                      {isAnalyzing ? (
                        <>
                          <Activity className="mr-2 h-5 w-5 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <PlayCircle className="mr-2 h-5 w-5" />
                          Start AI Analysis
                        </>
                      )}
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-8"
          >
            {/* Video Player */}
            <Card className="backdrop-blur-glass bg-card/90 border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <PlayCircle className="h-5 w-5" />
                  Analysis Video
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
                  <PlayCircle className="h-16 w-16 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>

            {/* Performance Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <Card className="backdrop-blur-glass bg-card/90 border-border/50">
                <CardHeader>
                  <CardTitle className="text-lg">Run-Up</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-primary mb-2">
                    {analysisResult.runUpAnalysis}%
                  </div>
                  <Progress value={analysisResult.runUpAnalysis} className="mb-2" />
                  <p className="text-sm text-muted-foreground">Consistent</p>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-glass bg-card/90 border-border/50">
                <CardHeader>
                  <CardTitle className="text-lg">Release Point</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-accent mb-2">
                    {analysisResult.releasePoint}
                  </div>
                  <Badge className="bg-accent text-accent-foreground">
                    Perfect
                  </Badge>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-glass bg-card/90 border-border/50">
                <CardHeader>
                  <CardTitle className="text-lg">Arm Angle</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-secondary mb-2">
                    {analysisResult.armAngle}°
                  </div>
                  <p className="text-sm text-muted-foreground">Ideal range</p>
                </CardContent>
              </Card>

              <Card className="backdrop-blur-glass bg-card/90 border-border/50">
                <CardHeader>
                  <CardTitle className="text-lg">Speed Est.</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2 mb-2">
                    <Zap className="h-6 w-6 text-accent" />
                    <div className="text-2xl font-bold text-accent">
                      {analysisResult.speedEstimation}
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">Fast-Medium</p>
                </CardContent>
              </Card>
            </div>

            {/* Bowling Type */}
            <Card className="backdrop-blur-glass bg-card/90 border-border/50">
              <CardHeader>
                <CardTitle>Bowling Analysis</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-muted-foreground mb-2">Bowling Type</p>
                  <Badge variant="secondary" className="text-lg px-4 py-2">
                    {analysisResult.bowlingType}
                  </Badge>
                </div>
                
                <div>
                  <p className="text-sm text-muted-foreground mb-2">Follow-Through Quality</p>
                  <div className="flex items-center gap-3">
                    <Progress value={analysisResult.followThrough} className="flex-1" />
                    <span className="font-bold">{analysisResult.followThrough}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Line & Length Heatmap */}
            <Card className="backdrop-blur-glass bg-card/90 border-border/50">
              <CardHeader>
                <CardTitle>Line & Length Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm">Good Length</span>
                      <span className="text-sm font-bold text-primary">
                        {analysisResult.lineAndLength.good}%
                      </span>
                    </div>
                    <Progress value={analysisResult.lineAndLength.good} />
                  </div>
                  
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm">Short</span>
                      <span className="text-sm font-bold text-secondary">
                        {analysisResult.lineAndLength.short}%
                      </span>
                    </div>
                    <Progress value={analysisResult.lineAndLength.short} />
                  </div>
                  
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm">Full</span>
                      <span className="text-sm font-bold text-accent">
                        {analysisResult.lineAndLength.full}%
                      </span>
                    </div>
                    <Progress value={analysisResult.lineAndLength.full} />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* AI Recommendations */}
            <Card className="backdrop-blur-glass bg-card/90 border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  AI Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analysisResult.recommendations.map((rec, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-3 bg-gradient-card rounded-lg">
                      <div className="h-6 w-6 rounded-full bg-primary/20 text-primary flex items-center justify-center text-sm font-bold">
                        {idx + 1}
                      </div>
                      <p className="text-sm flex-1">{rec}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Key Frames */}
            <Card className="backdrop-blur-glass bg-card/90 border-border/50">
              <CardHeader>
                <CardTitle>Action Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {analysisResult.keyFrames.map((frame, idx) => (
                    <div key={idx} className="aspect-video bg-muted rounded-lg overflow-hidden">
                      <img src={frame} alt={`Frame ${idx + 1}`} className="w-full h-full object-cover" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Button
              onClick={() => {
                setAnalysisResult(null);
                setSelectedFile(null);
                setUploadProgress(0);
              }}
              className="w-full max-w-md mx-auto block"
            >
              Analyze Another Video
            </Button>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default BowlingAnalysis;
