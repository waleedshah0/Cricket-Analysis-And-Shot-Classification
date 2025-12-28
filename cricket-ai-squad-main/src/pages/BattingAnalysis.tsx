import { useState, useEffect, useRef } from "react";
import { Navbar } from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Upload, PlayCircle, TrendingUp, Activity, Target } from "lucide-react";
import { motion } from "framer-motion";
import { useToast } from "@/hooks/use-toast";

interface AnalysisResult {
  shotsDetected: string[];
  shotTypeRecognition: string[];
  recommendations: string[];
  top3Predictions?: Array<{shotType: string; confidence: number}>;
}

const BattingAnalysis = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const { toast } = useToast();

  // Cleanup object URLs
  useEffect(() => {
    // Revoke the previous URL if it exists
    if (videoUrl) {
      URL.revokeObjectURL(videoUrl);
    }
    
    // Create new URL if a file is selected
    if (selectedFile) {
      const newUrl = URL.createObjectURL(selectedFile);
      setVideoUrl(newUrl);
      return () => URL.revokeObjectURL(newUrl);
    }
  }, [selectedFile]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Check MIME type
      const validMimeTypes = ["video/mp4", "video/quicktime", "video/x-msvideo"];
      
      // Check file extension as fallback
      const validExtensions = ['.mp4', '.mov', '.avi'];
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
      
      const isValidMimeType = validMimeTypes.includes(file.type);
      const isValidExtension = validExtensions.includes(fileExtension);
      
      // Accept file if either MIME type or extension is valid
      if (!isValidMimeType && !isValidExtension) {
        toast({
          title: "Invalid file type",
          description: `Please upload a .mp4, .mov, or .avi file. Detected file type: ${file.type || 'unknown'}`,
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

    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Send request to backend API
      const response = await fetch('http://localhost:8000/classify-video/', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Set analysis result from API response (removed footworkQuality, balanceAnalysis, timingClassification, and keyFrames)
      setAnalysisResult({
        shotsDetected: result.shotsDetected || [result.shotType],
        shotTypeRecognition: result.shotTypeRecognition || [`${result.shotType}: 100%`],
        recommendations: result.recommendations || [
          `Focus on improving your ${result.shotType} technique`,
          "Maintain proper body alignment during shots",
          "Keep practicing to refine your skills",
        ],
        top3Predictions: result.top3Predictions || [],
      });

      setIsAnalyzing(false);
      toast({
        title: "Analysis Complete!",
        description: `Your batting performance has been analyzed. Predicted shot: ${result.shotType} (${result.confidence}%)`,
      });
    } catch (error) {
      console.error('Error analyzing video:', error);
      setIsAnalyzing(false);
      toast({
        title: "Analysis Failed",
        description: "There was an error analyzing your video. Please try again.",
        variant: "destructive",
      });
    }
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
            AI Batting Performance Analyzer
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Upload your batting footage. AI will break down timing, footwork, balance & bat swing.
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
                <CardTitle>Upload Batting Video</CardTitle>
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
                <div className="aspect-video bg-muted rounded-lg overflow-hidden">
                  {videoUrl ? (
                    <video 
                      ref={videoRef}
                      src={videoUrl} 
                      controls 
                      className="w-full h-full object-contain"
                      onError={(e) => console.error('Error loading video:', e)}
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <PlayCircle className="h-16 w-16 text-muted-foreground" />
                      <span className="ml-4 text-muted-foreground">No video selected</span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Top 3 Predictions */}
            {analysisResult.top3Predictions && analysisResult.top3Predictions.length > 0 && (
              <Card className="backdrop-blur-glass bg-card/90 border-border/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5" />
                    Top 3 Predictions
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {analysisResult.top3Predictions.map((pred, idx) => (
                      <div key={idx} className="flex items-center justify-between p-4 bg-gradient-card rounded-lg border border-border/30">
                        <div className="flex items-center gap-3">
                          <div className="h-8 w-8 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-sm">
                            {idx + 1}
                          </div>
                          <span className="font-semibold text-foreground">{pred.shotType}</span>
                        </div>
                        <div className="text-right">
                          <span className="text-lg font-bold text-primary">{pred.confidence.toFixed(2)}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Shots Detected */}
            <Card className="backdrop-blur-glass bg-card/90 border-border/50">
              <CardHeader>
                <CardTitle>Shots Detected</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {analysisResult.shotsDetected.map((shot, idx) => (
                    <Badge key={idx} variant="secondary" className="text-sm">
                      {shot}
                    </Badge>
                  ))}
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

            <Button
              onClick={() => {
                setAnalysisResult(null);
                setSelectedFile(null);
                setUploadProgress(0);
                // Reset video playback if it exists
                if (videoRef.current) {
                  videoRef.current.pause();
                  videoRef.current.currentTime = 0;
                }
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

export default BattingAnalysis;
