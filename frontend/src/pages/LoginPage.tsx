import { TextField } from '@consta/uikit/TextField';
import { Button } from '@consta/uikit/Button';
import { useState } from 'react';
import { login } from '../api/auth';
import { useNavigate } from 'react-router-dom';

export const LoginPage = () => {
  const [loginValue, setLoginValue] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const data = await login(loginValue, password);
      if (data.role === 'admin') navigate('/admin');
      else if (data.role === 'observer') navigate('/observer');
      else navigate('/employee');
    } catch (error) {
      alert('Ошибка входа. Проверьте логин и пароль.');
    }
  };

  return (
    <div style={{ maxWidth: 320, margin: '100px auto' }}>
      <TextField label="Логин" value={loginValue} onChange={({ value }) => setLoginValue(value || '')} />
      <TextField
        label="Пароль"
        type="password"
        value={password}
        onChange={({ value }) => setPassword(value || '')}
      />
      <Button label="Войти" onClick={handleLogin} />
    </div>
  );
};
