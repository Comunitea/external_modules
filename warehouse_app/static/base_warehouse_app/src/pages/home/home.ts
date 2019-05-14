import { Component } from '@angular/core';

import { TranslateService } from '@ngx-translate/core';

import { IonicPage, NavController, ToastController } from 'ionic-angular';
import { Storage } from '@ionic/storage'
import { MainPage } from '../';
import { OdooProvider } from '../../providers/odoo/odoo'

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage {
  conexion = {
		url: 'http://192.168.0.121',
    port: '8069',
    db: 'lasrias',
    username: 'admin',
		password: 'admin',
		user: {}
  
  }
  cargar = false;
  
  // Our translated text strings
  private loginErrorString: string;

  constructor(public navCtrl: NavController, public storage: Storage, public translateService: TranslateService,
    private odoo: OdooProvider) {
     
  }

}
