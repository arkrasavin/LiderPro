import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { logout } from '@/routers/auth';

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <header className="flex justify-between items-center p-4 shadow bg-white">
      <h1 className="text-xl font-bold">Employee Tracker</h1>
      <Button variant="outline" onClick={handleLogout}>
        Выйти
      </Button>
    </header>
  );
};

export default Header;
