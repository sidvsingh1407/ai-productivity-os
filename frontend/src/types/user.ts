export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superadmin?: boolean;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  industry?: string;
  size?: string;
}
