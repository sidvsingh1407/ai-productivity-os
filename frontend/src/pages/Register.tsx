import { useState } from 'react';
import { useNavigate, Link, Navigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { authApi } from '@/api/auth';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { registerSchema, RegisterFormData } from '@/lib/schemas';

export function Register() {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { setAuth, isAuthenticated } = useAuthStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  if (isAuthenticated) {
    return <Navigate to="/app/dashboard" replace />;
  }

  const onSubmit = async (dataForm: RegisterFormData) => {
    setError('');
    setLoading(true);

    try {
      // 1. Attempt registration
      await authApi.register({
        full_name: dataForm.fullName,
        email: dataForm.email,
        password: dataForm.password,
        org_name: dataForm.companyName // Backend expects org_name, form uses companyName
      });

      // If we reach here, registration returned a 2xx success response.
      // 2. Attempt auto-login
      try {
        const loginData = await authApi.login({ email: dataForm.email, password: dataForm.password });
        setAuth(loginData.user, loginData.org, loginData.access_token, loginData.refresh_token);
        navigate('/app/dashboard');
      } catch (loginErr: any) {
        // If login fails due to required verification (403), we fall back to login page
        if (loginErr.response?.status === 403) {
          navigate('/login', { state: { message: "Registration successful. Please verify your email to login." } });
        } else {
          // If login fails for any other reason (500, timeout, etc.), display inline error
          setError(loginErr.response?.data?.detail || 'Registration successful, but failed to auto-login. Please try logging in manually.');
        }
      }
    } catch (err: any) {
      // If registration fails (e.g., 500 error, 400 validation error), catch it and display inline
      // For validation errors from backend, the response could be an array under detail
      if (Array.isArray(err.response?.data?.detail)) {
        setError(err.response.data.detail[0]?.msg || 'Validation error');
      } else {
        setError(err.response?.data?.detail || err.message || 'Failed to register. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/40 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold tracking-tight">Create an account</CardTitle>
          <CardDescription>
            Enter your information below to create your account
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit(onSubmit)}>
          <CardContent className="space-y-4">
            {error && <div className="text-sm font-medium text-destructive">{error}</div>}
            <div className="space-y-2">
              <Label htmlFor="fullName">Full Name</Label>
              <Input
                id="fullName"
                placeholder="John Doe"
                autoComplete="name"
                {...register('fullName')}
              />
              {errors.fullName && <span className="text-xs text-destructive">{errors.fullName.message}</span>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="companyName">Company Name</Label>
              <Input
                id="companyName"
                placeholder="Acme Corp"
                autoComplete="organization"
                {...register('companyName')}
              />
              {errors.companyName && <span className="text-xs text-destructive">{errors.companyName.message}</span>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                autoComplete="email"
                {...register('email')}
              />
              {errors.email && <span className="text-xs text-destructive">{errors.email.message}</span>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                autoComplete="new-password"
                {...register('password')}
              />
              {errors.password && <span className="text-xs text-destructive">{errors.password.message}</span>}
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Creating account...' : 'Create account'}
            </Button>
            <div className="text-center text-sm text-muted-foreground">
              Already have an account?{' '}
              <Link to="/login" className="text-primary hover:underline">
                Sign in
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
