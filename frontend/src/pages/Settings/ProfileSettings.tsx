import { useAuthStore } from '../../store/authStore';

export default function ProfileSettings() {
  const { user } = useAuthStore();

  return (
    <div className="bg-white shadow sm:rounded-lg mb-8" style={{ background: 'var(--tx-bg-card)', borderColor: 'var(--tx-border)' }}>
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900" style={{ color: 'var(--tx-text-primary)' }}>
          Profile Settings
        </h3>

        <div className="mt-5 border-t pt-5">
          <dl className="divide-y divide-gray-200">
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt className="text-sm font-medium text-gray-500" style={{ color: 'var(--tx-text-secondary)' }}>Full name</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2" style={{ color: 'var(--tx-text-primary)' }}>{user?.full_name}</dd>
            </div>
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt className="text-sm font-medium text-gray-500" style={{ color: 'var(--tx-text-secondary)' }}>Email address</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2" style={{ color: 'var(--tx-text-primary)' }}>
                {user?.email}
                {user?.email_verified === false && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                    Unverified
                  </span>
                )}
                {user?.email_verified && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Verified
                  </span>
                )}
              </dd>
            </div>
          </dl>
        </div>

      </div>
    </div>
  );
}
