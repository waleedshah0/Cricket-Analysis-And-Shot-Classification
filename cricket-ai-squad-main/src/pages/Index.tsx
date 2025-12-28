import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Sparkles, Target, TrendingUp, Users, Video, Activity } from "lucide-react";
import { motion } from "framer-motion";
import { Navbar } from "@/components/Navbar";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-hero relative overflow-hidden">
      {/* Animated particles background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-primary rounded-full"
            initial={{ 
              x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1000), 
              y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 1000),
              opacity: 0 
            }}
            animate={{ 
              y: [null, Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 1000)],
              opacity: [0, 1, 0],
            }}
            transition={{ 
              duration: Math.random() * 5 + 3,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
          />
        ))}
      </div>

      <Navbar />
      
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16 md:py-24 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-8"
        >
          <div className="inline-block">
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className="flex flex-col items-center justify-center gap-4 mb-6"
            >
              <Sparkles className="h-16 w-16 text-primary animate-pulse-glow" />
              <h1 className="text-5xl md:text-7xl font-poppins font-bold text-white text-glow-primary">
                AI Cricket Selector
              </h1>
              <h1 className="text-4xl md:text-6xl font-poppins font-bold text-white text-glow-secondary">
                & Performance Analyzer
              </h1>
            </motion.div>
          </div>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-xl md:text-2xl text-foreground max-w-3xl mx-auto leading-relaxed"
          >
            Get the perfect squad by ground & format. Analyze your batting and bowling with AI.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4 justify-center pt-8"
          >
            <Button 
              onClick={() => navigate("/generator")}
              className="bg-primary hover:bg-primary/90 text-background px-8 py-6 text-lg font-semibold shadow-neon-primary hover:shadow-glow-primary transition-all duration-300 hover:scale-105 border-glow-primary"
            >
              <Sparkles className="mr-2 h-6 w-6" />
              Generate Squad
            </Button>
            
            <Button 
              onClick={() => navigate("/analyze-batting")}
              className="bg-secondary hover:bg-secondary/90 text-white px-8 py-6 text-lg font-semibold shadow-neon-secondary hover:shadow-glow-secondary transition-all duration-300 hover:scale-105 border-glow-secondary"
            >
              <Video className="mr-2 h-6 w-6" />
              Analyze Batting
            </Button>
            
            <Button 
              onClick={() => navigate("/analyze-bowling")}
              className="bg-secondary hover:bg-secondary/90 text-white px-8 py-6 text-lg font-semibold shadow-neon-secondary hover:shadow-glow-secondary transition-all duration-300 hover:scale-105 border-glow-secondary"
            >
              <Activity className="mr-2 h-6 w-6" />
              Analyze Bowling
            </Button>
          </motion.div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24"
        >
          <motion.div
            whileHover={{ scale: 1.05, y: -5 }}
            className="glass-card rounded-2xl p-8 shadow-neon-primary transition-all duration-300 group"
          >
            <div className="bg-gradient-card rounded-full w-16 h-16 flex items-center justify-center mb-6 border border-primary/30 group-hover:border-primary group-hover:shadow-glow-primary transition-all">
              <Target className="h-8 w-8 text-primary" />
            </div>
            <h3 className="text-2xl font-poppins font-bold mb-3 text-white group-hover:text-glow-primary transition-all">Smart Selection</h3>
            <p className="text-muted-foreground leading-relaxed">
              AI-powered algorithm analyzes ground conditions, format, and player performance to suggest the optimal squad
            </p>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05, y: -5 }}
            className="glass-card rounded-2xl p-8 shadow-neon-secondary transition-all duration-300 group"
          >
            <div className="bg-gradient-card rounded-full w-16 h-16 flex items-center justify-center mb-6 border border-secondary/30 group-hover:border-secondary group-hover:shadow-glow-secondary transition-all">
              <TrendingUp className="h-8 w-8 text-secondary" />
            </div>
            <h3 className="text-2xl font-poppins font-bold mb-3 text-white group-hover:text-glow-secondary transition-all">Format-Specific</h3>
            <p className="text-muted-foreground leading-relaxed">
              Get tailored recommendations for Test, ODI, or T20I formats based on detailed player statistics
            </p>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05, y: -5 }}
            className="glass-card rounded-2xl p-8 shadow-neon-primary transition-all duration-300 group"
          >
            <div className="bg-gradient-card rounded-full w-16 h-16 flex items-center justify-center mb-6 border border-primary/30 group-hover:border-primary group-hover:shadow-glow-primary transition-all">
              <Users className="h-8 w-8 text-primary" />
            </div>
            <h3 className="text-2xl font-poppins font-bold mb-3 text-white group-hover:text-glow-primary transition-all">15-Player Squad</h3>
            <p className="text-muted-foreground leading-relaxed">
              Recommended playing XI plus 4 strategic backup players for comprehensive team coverage
            </p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Index;

