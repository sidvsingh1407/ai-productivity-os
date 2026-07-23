import React from 'react';
import ProfileSettings from './ProfileSettings';
import OrgSettings from './OrgSettings';
import EngineeringSettings from './EngineeringSettings';
import Billing from './Billing';
import AccountActions from './AccountActions';
import DangerZone from './DangerZone';

export default function SettingsPage() {
  return (
    <div className="space-y-12 max-w-4xl pb-12">
      <ProfileSettings />
      <OrgSettings />
      <EngineeringSettings />
      <Billing />
      <AccountActions />
      <DangerZone />
    </div>
  );
}
