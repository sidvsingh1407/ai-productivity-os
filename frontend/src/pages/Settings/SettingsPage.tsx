import React from 'react';
import OrgSettings from './OrgSettings';
import Billing from './Billing';
import DangerZone from './DangerZone';

export default function SettingsPage() {
  return (
    <div className="space-y-12 max-w-4xl pb-12">
      <OrgSettings />
      <Billing />
      <DangerZone />
    </div>
  );
}
