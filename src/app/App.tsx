import { StarField } from './components/StarField';
import { Navigation } from './components/Navigation';
import { Hero } from './components/Hero';
import { About } from './components/About';
import { Features } from './components/Features';
import { Crew } from './components/Crew';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div className="relative min-h-screen bg-[#0a0e27] text-white overflow-x-hidden">
      {/* Space background with stars */}
      <StarField />
      
      {/* Navigation */}
      <Navigation />
      
      {/* Main content */}
      <main className="relative z-10">
        <Hero />
        <About />
        <Features />
        <Crew />
      </main>
      
      {/* Footer */}
      <Footer />
    </div>
  );
}
