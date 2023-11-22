// Attendance Positions on Google maps
function attendancePositionsInitMap() {

    // List of positions
    var positions = []

    // Set var
    offset = new google.maps.Size(0, 46)
    toclaster = []
    // Map create
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
    });

    // attendance_id
    var attendance_id = $("#attendance_id").html();
    attendance_id = parseInt(attendance_id);

    var session = new openerp.Session();
    var attendance_obj = new openerp.Model(session, "hr.attendance");

    attendance_obj.call('get_attendance_data', [attendance_id]).then(function (attendance_data) {
            if (attendance_data['action'] == 'sign_out' && attendance_data['related_attendance_id']) {
                attendance_id = attendance_data['related_attendance_id'];
            }

            var attendance_position = new openerp.Model(session, "hr.attendance.position");

            attendance_position.query(['latitude', 'longitude', 'write_date'])
                .filter([['attendance_id', '=', attendance_id]])
                .all().then(function (positions_result) {
                    positions = positions_result

                    var polyline_coords = []

                    // Add shop's marker and info popup
                    const positions_len = positions.length;
                    var markers = positions.map(function(location, i){
                        
                        map_coords = {
                            'lat': location.latitude,
                            'lng': location.longitude
                        }

                        if(positions_len === i + 1) {
                            map.setCenter(map_coords);
                        }

                        polyline_coords.push(map_coords) ;

                        // Add marker
                        var marker = new google.maps.Marker({
                            position: map_coords,
                            map: map,
                            title: location.write_date,
                        });
                        toclaster.push(marker)
                        // Add info popup
                        var window = new google.maps.InfoWindow({
                            content: '<div><h3>Hora: '+location.write_date+'</h3></div>',
                            maxWidth: 250,
                            pixelOffset: offset
                        });
                        // Add marker click action
                        return marker.addListener('click', function() {
                            // map.setCenter(marker.getPosition())
                            // map.setZoom(18);
                            window.open(map, marker);
                        });
                    });

                    var polyline_line = new google.maps.Polyline({
                        path: polyline_coords,
                        geodesic: true,
                        strokeColor: '#FF0000',
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    });

                    polyline_line.setMap(map);
            
            });
    });

}
