import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';
import axios from 'axios';

// 可选：添加请求拦截器 - 例如添加认证 token
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// 可选：添加响应拦截器 - 例如统一处理错误
axios.interceptors.response.use(response => {
  return response;
}, error => {
  // 处理常见错误，如 401 未授权可能需要重定向到登录页面
  if (error.response && error.response.status === 401) {
    // 重定向到登录页或清除本地认证信息
    // window.location.href = '/login';
    localStorage.removeItem('authToken');
  }
  return Promise.reject(error);
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

const reportWebVitals = (onPerfEntry) => {
    if (onPerfEntry && onPerfEntry instanceof Function) {
        import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
        getCLS(onPerfEntry); // 累积布局偏移
        getFID(onPerfEntry); // 首次输入延迟
        getFCP(onPerfEntry); // 首次内容绘制
        getLCP(onPerfEntry); // 最大内容绘制
        getTTFB(onPerfEntry); // 首字节时间
        });
    }
};

export default reportWebVitals;

// 如果你想开始测量应用性能，传递一个函数
// 来记录结果（例如：reportWebVitals(console.log)）
// 或发送到分析端点。了解更多：https://bit.ly/CRA-vitals
reportWebVitals();