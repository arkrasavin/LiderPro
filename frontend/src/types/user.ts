export type UserRole = 'admin' | 'employee' | 'observer';

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
}

export interface Education {
  mentee_points: number;
  training_points1: number;
  training_points2: number;
}

export interface EmployeeInfo {
  employee: User;
  education: Education;
}
