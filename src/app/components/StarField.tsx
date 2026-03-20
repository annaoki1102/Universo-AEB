import { useEffect, useRef } from 'react';

export function StarField() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const setCanvasSize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    setCanvasSize();
    window.addEventListener('resize', setCanvasSize);

    // Create stars
    const stars: { x: number; y: number; radius: number; opacity: number; twinkleSpeed: number; brightness: number }[] = [];
    const starCount = 600; // Increased from 200

    for (let i = 0; i < starCount; i++) {
      const brightness = Math.random();
      let radius;
      
      // Create variation in star sizes for depth
      if (brightness > 0.9) {
        radius = 1.5 + Math.random() * 1; // Brighter, larger stars
      } else if (brightness > 0.7) {
        radius = 1 + Math.random() * 0.5; // Medium stars
      } else {
        radius = 0.5 + Math.random() * 0.5; // Smaller, dimmer stars
      }
      
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: radius,
        opacity: 0.3 + Math.random() * 0.7,
        twinkleSpeed: 0.005 + Math.random() * 0.015,
        brightness: brightness,
      });
    }

    // Animation
    let animationId: number;
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      stars.forEach((star) => {
        // Twinkle effect
        star.opacity += star.twinkleSpeed;
        if (star.opacity > 1 || star.opacity < 0.3) {
          star.twinkleSpeed *= -1;
        }

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        
        // Vary color and intensity based on brightness
        if (star.brightness > 0.9) {
          // Brighter stars with slight blue-white tint
          ctx.fillStyle = `rgba(220, 235, 255, ${star.opacity})`;
        } else if (star.brightness > 0.7) {
          // Medium brightness with cyan tint
          ctx.fillStyle = `rgba(200, 225, 255, ${star.opacity * 0.9})`;
        } else {
          // Dimmer stars for depth
          ctx.fillStyle = `rgba(180, 200, 230, ${star.opacity * 0.7})`;
        }
        
        ctx.fill();
        
        // Add subtle glow to brightest stars
        if (star.brightness > 0.95 && star.opacity > 0.8) {
          ctx.shadowBlur = 3;
          ctx.shadowColor = 'rgba(200, 230, 255, 0.5)';
          ctx.fill();
          ctx.shadowBlur = 0;
        }
      });

      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', setCanvasSize);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 0 }}
    />
  );
}