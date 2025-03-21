import React from "react";
import { ApiKeyModal } from "./components/ApiKeyModal";
import { authApi } from "@/api";

type ApiKeyModalState = {
  open: boolean;
  apiKey: string;
};

export const ApiKeySection = () => {
  const [{ open, apiKey }, setModalState] = React.useState<ApiKeyModalState>({
    open: false,
    apiKey: "",
  });

  const handleApiKeyGenerate = async () => {
    const result = await authApi.createApiKey();
    if (result.isFailure) {
      return;
    }
    const createdApiKey = result.getValue().data;
    setModalState({ open: true, apiKey: createdApiKey });
  };
  return (
    <div>
      <button onClick={handleApiKeyGenerate}>Generate</button>
      <ApiKeyModal
        open={open}
        apiKey={apiKey}
        onClose={() => setModalState({ open: false, apiKey: "" })}
      />
    </div>
  );
};

export const SettingsPage = () => {
  return (
    <div>
      <h1>Settings</h1>
      <ApiKeySection />
    </div>
  );
};
