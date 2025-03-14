export class UserEntity {
  public id: string;
  public email: string;

  constructor(id: string, email: string) {
    this.email = email;
    this.id = id;
  }
}
