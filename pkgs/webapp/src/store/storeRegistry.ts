import { Store } from "redux";
import { GlobalState } from "./";

export class StoreRegistry {
  public store!: Store<GlobalState>;
  public register(store: Store<GlobalState>) {
    this.store = store;
  }
}

export const storeRegistry = new StoreRegistry();
