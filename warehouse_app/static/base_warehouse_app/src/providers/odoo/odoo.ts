import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage';

/*
  Generated class for the OdooProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
declare var OdooApi: any;

@Injectable()
export class OdooProvider {

    context
    uid
    constructor(private storage: Storage) {
      this.context = {'lang': 'es_ES', 'from_pda': true}
      this.uid = 0
    }

    login(user, password){
        var method = method
        var values = values
        var self = this
        var promise = new Promise( (resolve, reject) => {
            self.storage.get('CONEXION').then((con_data) => {
                var odoo = new OdooApi(con_data.url, con_data.db);
                // this.navCtrl.setRoot(HomePage, {borrar: true, login: null});
                if (con_data == null) {
                    var err = {'title': 'Error!', 'msg': 'No hay datos para establecer la conexión'}
                    reject(err);
                } else {

                    odoo.login(con_data.username, con_data.password).then( (uid) => {
                    self.uid = uid
                    resolve(uid)
                    })
                    .catch( (mierror) => {
                      var err = {'title': 'Error!', 'msg': 'No se pudo conectar con Odoo'}
                      reject(err);
                    });
                }
            });
        });
        return promise
    }

    execute(model, method, values) {

        var method = method
        var values = values
        var self = this
        var promise = new Promise( (resolve, reject) => {
            self.storage.get('CONEXION').then((con_data) => {
                var odoo = new OdooApi(con_data.url, con_data.db);
                odoo.context = self.context
                // this.navCtrl.setRoot(HomePage, {borrar: true, login: null});
                if (con_data == null) {
                    var err = {'title': 'Error!', 'msg': 'No hay datos para establecer la conexión'}
                    reject(err);
                } else {
                    odoo.login(con_data.username, con_data.password).then((uid) => {
                            odoo.call(model, method, values).then((res) => {
                                resolve(res);
                            })
                            .catch( () => {
                                var err = {'title': 'Error!', 'msg': 'Fallo al llamar al método ' + method + 'del modelo app.regustry'}
                                reject(err);
                            });
                    })
                    .catch( () => {
                        var err = {'title': 'Error!', 'msg': 'No se pudo conectar con Odoo'}
                        reject(err);
                    });
                }
            });
        });
        return promise
    }
    /*domain=None, fields=None, offset=0, limit=None, order=None, context=None*/
    write (model, id, data){

        var self = this
        var promise = new Promise( (resolve, reject) => {
            self.storage.get('CONEXION').then((con_data) => {
                var odoo = new OdooApi(con_data.url, con_data.db);
                odoo.context = self.context
                if (con_data == null) {
                    var err = {'title': 'Error!', 'msg': 'No hay datos para establecer la conexión'}
                    reject(err);
                } else {
                    odoo.login(con_data.username, con_data.password).then( (uid) => {
                        odoo.write(model, id, data).then((res) => {
                            resolve(res);
                        })
                        .catch( () => {
                            var err = {'title': 'Error!', 'msg': 'Fallo al llamar al hacer un write'}
                            reject(err);
                        });
                    })
                    .catch( () => {
                        var err = {'title': 'Error!', 'msg': 'No se pudo conectar con Odoo'}
                        reject(err);
                    });
                }
            });
        });
        return promise
    }
    searchRead_2(model, domain, fields, offset = 0, limit = 0, order = ''){
      var model = model;
      var domain = domain;
      var fields = fields;
      var self = this
      var promise = new Promise( (resolve, reject) => {
          self.storage.get('CONEXION').then((con_data) => {
              var odoo = new OdooApi(con_data.url, con_data.db);
              odoo.context = self.context
              if (con_data == null) {
                  var err = {'title': 'Error!', 'msg': 'No hay datos para establecer la conexión'}
                  reject(err);
              } else {
                odoo.uid = this
                odoo.search_read(model, domain, fields, offset, limit, order).then((res) => {
                    resolve(res);
                })
                .catch( () => {
                    var err = {'title': 'Error!', 'msg': 'Fallo al llamar al hacer search_read'}
                    reject(err);
                });

              }
          });
      });
      return promise
  }



    searchRead(model, domain, fields, offset = 0, limit = 0, order = ''){
        var model = model;
        var domain = domain;
        var fields = fields;
        var self = this
        var promise = new Promise( (resolve, reject) => {
            self.storage.get('CONEXION').then((con_data) => {

                if (con_data == null) {
                    var err = {'title': 'Error!', 'msg': 'No hay datos para establecer la conexión'}
                    reject(err);
                } else {
                    var odoo = new OdooApi(con_data.url, con_data.db);
                    odoo.context = self.context
                    odoo.login(con_data.username, con_data.password).then( (uid) => {

                    odoo.search_read(model, domain, fields, offset, limit, order).then((res) => {
                        resolve(res);
                    })
                    .catch( () => {
                        var err = {'title': 'Error!', 'msg': 'Fallo al llamar al hacer search_read'}
                        reject(err);
                    });
                    })
                    .catch( () => {
                        var err = {'title': 'Error!', 'msg': 'No se pudo conectar con Odoo'}
                        reject(err);
                    });
                }
            });
        });
        return promise
    }

}
