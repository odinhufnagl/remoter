import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { authReducer, State as AuthState } from "./auth/reducer";
import createSagaMiddleware from "redux-saga";
import rootSaga from "./sagas";
import { storeRegistry } from "./storeRegistry";

export interface GlobalState {
  auth: AuthState;
}

export const getGlobalState = (state: GlobalState): GlobalState => state;

const sagaMiddleware = createSagaMiddleware();

export const store = configureStore({
  reducer: combineReducers({
    auth: authReducer,
  }),
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(sagaMiddleware),
  devTools: process.env.NODE_ENV !== "production",
});

sagaMiddleware.run(rootSaga);
storeRegistry.register(store);
