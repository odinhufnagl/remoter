import React from "react";

import Modal from "@mui/material/Modal";
import { Box, Fade, Typography } from "@mui/material";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

type ApiKeyModalProps = {
  open: boolean;
  onClose: () => void;
  apiKey: string;
};

export const ApiKeyModal = ({ open, onClose, apiKey }: ApiKeyModalProps) => {
  return (
    <Modal open={open} onClose={onClose}>
      <Fade in={open}>
        <Box sx={style}>
          <Typography id="transition-modal-title" variant="h6" component="h2">
            This is your API key, keep it safe! You wont be able to see it
            again.
          </Typography>
          <Typography id="transition-modal-description" sx={{ mt: 2 }}>
            {apiKey}
          </Typography>
        </Box>
      </Fade>
    </Modal>
  );
};
