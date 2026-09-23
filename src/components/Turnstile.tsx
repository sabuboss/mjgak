"use client";

import { useCallback, useEffect, useRef, useState } from "react";

declare global {
  interface Window {
    turnstile?: {
      render: (el: HTMLElement, opts: Record<string, unknown>) => string;
      reset: (id: string) => void;
    };
  }
}

const SCRIPT = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";

/**
 * Cloudflare Turnstile 훅. siteKey 가 없으면 비활성(getToken → null).
 * 토큰은 1회용이라 요청 후 consume() 으로 리셋한다.
 */
export function useTurnstile(siteKey?: string) {
  const enabled = Boolean(siteKey);
  const containerRef = useRef<HTMLDivElement>(null);
  const widgetId = useRef<string | null>(null);
  const tokenRef = useRef<string | null>(null);
  const waiters = useRef<((t: string) => void)[]>([]);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (!enabled || !containerRef.current) return;
    const el = containerRef.current;
    function render() {
      if (!window.turnstile || widgetId.current) return;
      widgetId.current = window.turnstile.render(el, {
        sitekey: siteKey,
        theme: "light",
        size: "normal",
        callback: (t: string) => {
          tokenRef.current = t;
          waiters.current.forEach((w) => w(t));
          waiters.current = [];
        },
        "expired-callback": () => {
          tokenRef.current = null;
        },
        "error-callback": () => setFailed(true),
      });
    }
    if (window.turnstile) {
      render();
      return;
    }
    let s = document.querySelector<HTMLScriptElement>(`script[src="${SCRIPT}"]`);
    if (!s) {
      s = document.createElement("script");
      s.src = SCRIPT;
      s.async = true;
      document.head.appendChild(s);
    }
    s.addEventListener("load", render);
    return () => s?.removeEventListener("load", render);
  }, [enabled, siteKey]);

  const getToken = useCallback((): Promise<string | null> => {
    if (!enabled) return Promise.resolve(null);
    if (tokenRef.current) return Promise.resolve(tokenRef.current);
    return new Promise((res) => waiters.current.push(res));
  }, [enabled]);

  const consume = useCallback(() => {
    tokenRef.current = null;
    if (widgetId.current && window.turnstile) window.turnstile.reset(widgetId.current);
  }, []);

  const element = enabled ? (
    <div className="space-y-1">
      <div ref={containerRef} className="min-h-[65px]" />
      {failed && <p className="text-xs text-red-600">보안 확인 위젯을 불러오지 못했어요. 새로고침해 주세요.</p>}
    </div>
  ) : null;

  return { enabled, getToken, consume, element };
}
