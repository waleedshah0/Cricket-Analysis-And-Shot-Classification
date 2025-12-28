import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Home, Search } from "lucide-react";

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-hero p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center space-y-6"
      >
        <motion.div
          animate={{ rotate: [0, 5, -5, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="text-9xl"
        >
          🏏
        </motion.div>
        <h1 className="text-6xl font-bold text-white">404</h1>
        <h2 className="text-3xl font-semibold text-white">Out of Bounds!</h2>
        <p className="text-white/80 max-w-md text-lg">
          This page went for a six and never came back. Let's get you back to the pavilion.
        </p>
        <div className="flex gap-4 justify-center">
          <Button asChild size="lg" className="gap-2">
            <Link to="/">
              <Home className="h-5 w-5" />
              Go Home
            </Link>
          </Button>
          <Button asChild size="lg" variant="secondary" className="gap-2">
            <Link to="/generator">
              <Search className="h-5 w-5" />
              Generate Squad
            </Link>
          </Button>
        </div>
      </motion.div>
    </div>
  );
};

export default NotFound;

