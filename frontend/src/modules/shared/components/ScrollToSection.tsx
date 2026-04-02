import { useEffect } from "react";
import { useLocation } from "react-router-dom";

export function ScrollToSection() {
  const location = useLocation();

  useEffect(() => {
    const hash = location.hash;

    if (hash) {
      const id = hash.replace("#", "");

      setTimeout(() => {
        const element = document.getElementById(id);

        if (element) {
          element.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }, 200);
    } else {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    }
  }, [location]);

  return null;
}