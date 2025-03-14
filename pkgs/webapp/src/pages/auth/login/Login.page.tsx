import { authService } from "@/services/AuthService";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    const result = await authService.login({ email, password });
    if (result.isFailure) {
      setIsLoading(false);
      setError(result.errorValue()?.message || "Unknown error");
      return;
    }
    setIsLoading(false);
    navigate("/app");
  };

  return (
    <div>
      <h1>Login</h1>
      <h3>{isLoading && "Loading"}</h3>
      <h3>{error !== "" && error}</h3>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};
