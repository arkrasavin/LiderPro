import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

type Props = {
  title?: string;
  labels: string[];
  data: number[];
};

const Chart = ({ title = 'График', labels, data }: Props) => {
  const chartData = {
    labels,
    datasets: [
      {
        label: title,
        data,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  return <Line data={chartData} />;
};

export default Chart;
