import React from 'react';
import ProfileSettings from './ProfileSettings';
import OrgSettings from './OrgSettings';
import Billing from './Billing';
import DangerZone from './DangerZone';

export default function SettingsPage() {
  return (
    <div className="space-y-12 max-w-4xl pb-12">
      <ProfileSettings />
      <OrgSettings />
      <Billing />
      <DangerZone />
    </div>
  );
}
