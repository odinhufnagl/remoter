export abstract class TokenService {
  public abstract key: string;
  public save(token: string) {
    return localStorage.setItem(this.key, token);
  }
  public get(): string | null {
    return localStorage.getItem(this.key);
  }
  public remove() {
    return localStorage.removeItem(this.key);
  }
}
