import React from 'react';

const Welcome = ({ username }) => {
  return (
    <div>
      <h1>你好，{username}！</h1>
    </div>
  );
};

export default Welcome;
