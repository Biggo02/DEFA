import React from 'react';
import { DEFA_ROUTE_MANIFEST, resolveDefaRoute } from './routeManifest';

/**
 * Adapter for the legacy router. Import this component from the existing
 * entry point instead of replacing the monolithic router in one operation.
 * Screen components can be supplied by the caller so existing pages remain
 * untouched during the migration.
 */
export function DefaRouteAdapter({ pathname = window.location.pathname, screens = {}, fallback = null }) {
  const match = resolveDefaRoute(pathname);
  if (!match) return fallback;
  const Screen = screens[match.screen];
  if (!Screen) return fallback;
  return <Screen role={match.role} pathname={pathname} />;
}

export { DEFA_ROUTE_MANIFEST };
