import { ScrollToSection } from './components/ScrollToSection';
import { StarField } from './components/StarField';
import { Navigation } from './components/Navigation';
import { Hero } from './components/Hero';
import { About } from './components/About';
import { Features } from './components/Features';
import { Crew } from './components/Crew';
import { Footer } from './components/Footer';

import { Routes, Route } from "react-router-dom";
import Assistentes from "../pages/Assistentes";

export default function App() {
  return (
    <div className="relative min-h-screen bg-[#0a0e27] text-white overflow-x-hidden">
      <ScrollToSection />
      <StarField />
      <Navigation />

      <main className="relative z-10">
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Hero />
                <About />
                <Features />
                <Crew />
              </>
            }
          />
          <Route path="/assistentes" element={<Assistentes />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}