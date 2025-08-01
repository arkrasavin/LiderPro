import { useEffect, useState } from 'react';
import { getEmployeeData } from '../api/employee';
import Header from '../components/Header';
import Chart from '../components/Chart';

export const EmployeeDashboard = () => {
  const [employee, setEmployee] = useState<any>(null);

  useEffect(() => {
    getEmployeeData().then(setEmployee).catch(() => alert('Ошибка загрузки данных'));
  }, []);

  if (!employee) return <div>Загрузка...</div>;

  return (
    <div>
      <Header />
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-2">Добро пожаловать, {employee.employee.name}</h2>
        <p>Должность: {employee.employee.position}</p>
        <Chart
          title="Баллы обучения"
          labels={['Менторство', 'Тренинг 1', 'Тренинг 2']}
          data={[
            employee.education.mentee_points,
            employee.education.training_points1,
            employee.education.training_points2,
          ]}
        />
      </div>
    </div>
  );
};
