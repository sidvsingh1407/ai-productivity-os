import React, { useEffect, useRef } from 'react';

const TAU = Math.PI * 2;

const NODES = [
  { label: 'AI Governance',      sub: 'No escalation path defined',     angle: 0.30, dist: 112, sev: 'critical', phase: 0.0, size: 7 },
  { label: 'Workflow Handoffs',  sub: '2.4 day avg delay flagged',       angle: 1.05, dist: 82,  sev: 'warning',  phase: 0.7, size: 5 },
  { label: 'ROI Tracking',       sub: 'Passing — 78/100',                angle: 2.00, dist: 128, sev: 'ok',       phase: 1.4, size: 4 },
  { label: 'Adoption Rate',      sub: '34% — below threshold',           angle: 3.00, dist: 94,  sev: 'warning',  phase: 2.1, size: 5 },
  { label: 'Integration Layer',  sub: 'Stable across all services',      angle: 3.80, dist: 70,  sev: 'ok',       phase: 2.8, size: 4 },
  { label: 'Escalation Paths',   sub: 'Missing in 2 departments',        angle: 4.70, dist: 118, sev: 'critical', phase: 3.5, size: 7 },
  { label: 'Data Quality',       sub: 'Passing — clean pipeline',        angle: 5.50, dist: 60,  sev: 'ok',       phase: 4.2, size: 4 },
  { label: 'Process Docs',       sub: '3 governance gaps found',         angle: 1.75, dist: 142, sev: 'warning',  phase: 4.9, size: 5 },
  { label: 'AI Stack Audit',     sub: 'Stable — reviewed last cycle',    angle: 0.70, dist: 56,  sev: 'ok',       phase: 0.4, size: 4 },
  { label: 'Gov Review Cadence', sub: 'Overdue by 6 weeks',              angle: 5.90, dist: 132, sev: 'critical', phase: 1.1, size: 6 },
  { label: 'Compliance Flags',   sub: '2 active flags',                  angle: 2.30, dist: 155, sev: 'warning',  phase: 1.7, size: 5 },
  { label: 'AI Stack',           sub: 'Stable — passing',                angle: 0.90, dist: 58,  sev: 'ok',       phase: 0.9, size: 4 },
];

const SEV_COLOR = {
  critical: '#DC2626',
  warning:  '#D97706',
  ok:       '#059669',
};

interface ConstellationMapProps {
  variant?: 'hero' | 'about';
  height?: number;
}

export default function ConstellationMap({
  variant = 'hero',
  height = 420,
}: ConstellationMapProps) {
  const canvasRef  = useRef<HTMLCanvasElement>(null);
  const rafRef     = useRef(0);
  const starsRef   = useRef<{x: number, y: number, r: number, a: number, tw: number}[]>([]);
  const tooltipRef = useRef({ visible: false, x: 0, y: 0, node: null as any, alpha: 0 });

  useEffect(() => {
    const cv  = canvasRef.current;
    if (!cv) return;
    const ctx = cv.getContext('2d');
    if (!ctx) return;

    const resize = () => {
      const rect = cv.getBoundingClientRect();
      const dpr  = window.devicePixelRatio || 1;
      cv.width   = rect.width  * dpr;
      cv.height  = rect.height * dpr;
      ctx.scale(dpr, dpr);
      starsRef.current = Array.from({ length: 140 }, () => ({
        x:  Math.random() * rect.width,
        y:  Math.random() * rect.height,
        r:  Math.random() * 0.9 + 0.1,
        a:  Math.random() * 0.45 + 0.08,
        tw: Math.random() * TAU,
      }));
    };

    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(cv);

    /* hover tooltip — about variant only */
    const onMouseMove = (e: MouseEvent) => {
      if (variant !== 'about') return;
      const rect = cv.getBoundingClientRect();
      const mx   = (e.clientX - rect.left);
      const my   = (e.clientY - rect.top);
      const W    = rect.width;
      const H    = rect.height;
      const cx   = W / 2;
      const cy   = H / 2;
      const ds   = Math.min(W, H) / 380;
      const ang  = (performance.now() * 0.0018) * 0.22;
      let found: any = null;
      NODES.forEach(node => {
        const a  = node.angle + ang;
        const nx = cx + Math.cos(a) * node.dist * ds * 0.78;
        const ny = cy + Math.sin(a) * node.dist * ds * 0.54;
        const d  = Math.sqrt((mx - nx) ** 2 + (my - ny) ** 2);
        if (d < 14) found = { node, nx, ny };
      });
      if (found) {
        tooltipRef.current = { visible: true, x: found.nx, y: found.ny, node: found.node, alpha: tooltipRef.current.alpha };
      } else {
        tooltipRef.current.visible = false;
      }
    };

    cv.addEventListener('mousemove', onMouseMove);

    let startTime = 0;

    const loop = (now: number) => {
      if (!startTime) startTime = now;
      const t    = now - startTime;
      const rect = cv.getBoundingClientRect();
      const W    = rect.width;
      const H    = rect.height;
      const cx   = W / 2;
      const cy   = H / 2;
      const ds   = Math.min(W, H) / 380;

      ctx.clearRect(0, 0, W, H);

      /* bg */
      ctx.fillStyle = '#0B1F3A';
      ctx.fillRect(0, 0, W, H);

      /* vignette */
      const vg = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(W, H) * 0.72);
      vg.addColorStop(0, 'rgba(37,99,235,0.04)');
      vg.addColorStop(1, 'rgba(6,15,28,0.5)');
      ctx.fillStyle = vg;
      ctx.fillRect(0, 0, W, H);

      /* stars */
      starsRef.current.forEach(s => {
        const tw = Math.sin(t * 0.015 + s.tw) * 0.25 + 0.75;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, TAU);
        ctx.fillStyle = `rgba(255,253,249,${s.a * tw})`;
        ctx.fill();
      });

      /* orbit rings */
      [52, 82, 112, 142, 172].forEach((r, i) => {
        ctx.beginPath();
        ctx.arc(cx, cy, r * ds, 0, TAU);
        ctx.strokeStyle = `rgba(37,99,235,${0.05 + i * 0.012})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      });

      const ang = t * 0.0018 * 0.22;

      /* connection lines */
      NODES.forEach(node => {
        const a  = node.angle + ang;
        const nx = cx + Math.cos(a) * node.dist * ds * 0.78;
        const ny = cy + Math.sin(a) * node.dist * ds * 0.54;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(nx, ny);
        ctx.strokeStyle = SEV_COLOR[node.sev as keyof typeof SEV_COLOR] + '18';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      });

      /* nodes */
      NODES.forEach(node => {
        const a     = node.angle + ang;
        const nx    = cx + Math.cos(a) * node.dist * ds * 0.78;
        const ny    = cy + Math.sin(a) * node.dist * ds * 0.54;
        const col   = SEV_COLOR[node.sev as keyof typeof SEV_COLOR];
        const pulse = Math.sin(t * 0.032 + node.phase) * 0.5 + 0.5;

        if (node.sev === 'critical') {
          ctx.beginPath();
          ctx.arc(nx, ny, (node.size + 4 + pulse * 7) * ds, 0, TAU);
          ctx.fillStyle = col + '10';
          ctx.fill();
          ctx.beginPath();
          ctx.arc(nx, ny, (node.size + 3) * ds, 0, TAU);
          ctx.strokeStyle = col;
          ctx.lineWidth = 0.8;
          ctx.globalAlpha = 0.28 + pulse * 0.42;
          ctx.stroke();
          ctx.globalAlpha = 1;
        }

        ctx.beginPath();
        ctx.arc(nx, ny, node.size * ds, 0, TAU);
        ctx.fillStyle = col;
        ctx.globalAlpha = 0.78 + pulse * 0.22;
        ctx.fill();
        ctx.globalAlpha = 1;

        /* labels */
        if (W > 280) {
          ctx.font = `${Math.max(8, 9 * ds)}px Inter, sans-serif`;
          ctx.fillStyle = node.sev === 'critical'
            ? `rgba(220,38,38,${0.72 + pulse * 0.28})`
            : 'rgba(100,116,139,0.82)';
          ctx.textAlign = nx < cx ? 'right' : 'left';
          const ox = (nx < cx ? -11 : 11) * ds;
          ctx.fillText(node.label, nx + ox, ny + 3);
        }
      });

      /* tooltip — about variant */
      if (variant === 'about') {
        const tip = tooltipRef.current;
        if (tip.visible && tip.node) {
          tip.alpha = Math.min(1, tip.alpha + 0.08);
        } else {
          tip.alpha = Math.max(0, tip.alpha - 0.06);
        }
        if (tip.alpha > 0 && tip.node) {
          const col = SEV_COLOR[tip.node.sev as keyof typeof SEV_COLOR];
          const tx2 = tip.x > cx ? tip.x - 158 : tip.x + 14;
          const ty2 = tip.y - 44;
          ctx.globalAlpha = tip.alpha;
          ctx.fillStyle = 'rgba(15,23,42,0.95)';
          ctx.beginPath();
          ctx.roundRect(tx2, ty2, 152, 54, 6);
          ctx.fill();
          ctx.strokeStyle = col + '55';
          ctx.lineWidth = 0.8;
          ctx.stroke();
          ctx.font = '500 11px Inter, sans-serif';
          ctx.fillStyle = '#fffdf9';
          ctx.textAlign = 'left';
          ctx.fillText(tip.node.label, tx2 + 10, ty2 + 18);
          ctx.font = '10px Inter, sans-serif';
          ctx.fillStyle = '#64748B';
          ctx.fillText(tip.node.sub, tx2 + 10, ty2 + 33);
          ctx.font = '500 9px IBM Plex Mono, monospace';
          ctx.fillStyle = col;
          ctx.fillText(tip.node.sev.toUpperCase(), tx2 + 10, ty2 + 47);
          ctx.globalAlpha = 1;
        }
      }

      /* core */
      const cp = Math.sin(t * 0.022) * 0.5 + 0.5;
      ctx.beginPath();
      ctx.arc(cx, cy, (20 + cp * 5) * ds, 0, TAU);
      ctx.fillStyle = 'rgba(37,99,235,0.09)';
      ctx.fill();
      ctx.beginPath();
      ctx.arc(cx, cy, 14 * ds, 0, TAU);
      ctx.fillStyle = '#060F1C';
      ctx.fill();
      ctx.strokeStyle = '#2563EB';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.font = `500 ${Math.max(8, 10 * ds)}px IBM Plex Mono, monospace`;
      ctx.fillStyle = '#2563EB';
      ctx.textAlign = 'center';
      ctx.fillText('TX', cx, cy + 3 * ds);

      rafRef.current = requestAnimationFrame(loop);
    };

    rafRef.current = requestAnimationFrame(loop);
    return () => {
      cancelAnimationFrame(rafRef.current);
      ro.disconnect();
      cv.removeEventListener('mousemove', onMouseMove as EventListener);
    };
  }, [variant]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        display:  'block',
        width:    '100%',
        height:   height,
        cursor:   variant === 'about' ? 'crosshair' : 'default',
      }}
    />
  );
}
