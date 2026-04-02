import { createBrowserRouter } from "react-router-dom";
import { ScrollToSection } from "../modules/shared/components/ScrollToSection";
import { StarField } from "../modules/shared/components/StarField";
import { Navigation } from "../modules/shared/components/Navigation";
import { Hero } from "../modules/shared/components/Hero";
import { About } from "../modules/shared/components/About";
import { Features } from "../modules/shared/components/Features";
import { Crew } from "../modules/shared/components/Crew";
import { Footer } from "../modules/shared/components/Footer";
import Assistentes from "../modules/assistentes/pages/Assistentes";

function HomePage() {
  return (
    <div className="relative min-h-screen bg-[#0a0e27] text-white overflow-x-hidden">
      <ScrollToSection />
      <StarField />
      <Navigation />

      <main className="relative z-10">
        <Hero />
        <About />
        <Features />
        <Crew />
      </main>

      <Footer />
    </div>
  );
}

function AssistentesPage() {
  return <Assistentes />;
}

export const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/assistentes",
    element: <AssistentesPage />,
  },
]);
