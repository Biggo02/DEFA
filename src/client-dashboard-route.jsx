import React from 'react';
import ClientDashboardLive from './ClientDashboardLive';

/**
 * Drop-in route component for the existing React router.
 * Mount this component on the existing client dashboard path.
 */
export default function ClientDashboardRoute() {
  return <ClientDashboardLive />;
}
