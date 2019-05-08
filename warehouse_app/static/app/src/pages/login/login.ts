import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { IonicPage, NavController, ToastController } from 'ionic-angular';

import { User } from '../../providers';
import { MainPage } from '../';
import { OdooProvider } from '../../providers/odoo/odoo'

@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html'
})
export class LoginPage {
  // The account fields for the login form.
  // If you're using the username field with or without email, make
  // sure to add it to the type
  account: { email: string, password: string, database: string, url: string, port: number } = {
    email: 'test@example.com',
    password: 'test',
    database: 'database',
    url: 'http://192.168.0.121',
    port: 8069
  };

  // Our translated text strings
  private loginErrorString: string;

  constructor(public navCtrl: NavController,
    public user: User,
    public toastCtrl: ToastController,
    public translateService: TranslateService,
    private odoo: OdooProvider) {

    this.translateService.get('LOGIN_ERROR').subscribe((value) => {
      this.loginErrorString = value;
    })
  }

  // Attempt to login in through our User service
  doLogin() {
    this.user.login(this.account).subscribe((resp) => {
      this.navCtrl.push(MainPage);
    }, (err) => {
      this.navCtrl.push(MainPage);
      // Unable to log in
      let toast = this.toastCtrl.create({
        message: this.loginErrorString,
        duration: 3000,
        position: 'top'
      });
      toast.present();
    });
  }

  check_conexion(con) {	
		var model = 'res.users'
		var domain = [['login', '=', con.username]]
		var fields = ['id', 'login', 'image', 'name', 'company_id']
		this.odoo.login(con.username, con.password).then ((uid)=>{
			this.odoo.uid = uid
			this.odoo.searchRead(model, domain, fields).then((value)=>{
				var user = {id: null, name: null, image: null, login: null, cliente_id: null, company_id: null};
				if (value) {
					if (!con.user || value[0].id != con.user['id'] || value[0].company_id[0] != con.user['company_id']){
						user = value[0];
						//user.id = value[0].id;
						//user.name = value[0].name;
						//user.login = value[0].login;
						//user.company_id = value[0].company_id[0];
						//user.company = value[0].company_id
						con.user = user
					}
					this.storage.set('CONEXION', con).then(()=>{
						this.navCtrl.setRoot(TreepickPage);
					})
				}})
			.catch(() => {
				this.cargar = false;
				this.presentAlert('Error!', 'No se pudo encontrar el usuario:' + con.username);
			});
		})
		.catch (()=>{
			this.presentAlert('Error!', 'No se pudo conectar a Odoo');
			this.cargar = false;
		})
	}
}
