<?php
$servername = "172.16.1.139";
$username = "miusuario";
$password = "misuperpassword";
$dbname = "catalogocentralizado";

$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$url = "https://listado-siagro.conabio.gob.mx/api/graphql";
$query = 'query {
		agrobiodiversidads(pagination:{limit:5000} 
		  search:{operator:and search:[
			{field:id, value:"%pendiente%", operator:notLike}, 
			{field:es_parientesilvestre, value:"true", operator: eq},
			{field:estatus, value:"Aceptado/Válido", operator: eq}
			
		  
		  ]})
		  { 
			id
			taxon_valido
			es_parientesilvestre    
		  }
	}';
$data = array ('query' => $query);
$data = http_build_query($data);
$arrContextOptions=array(
    "ssl"=>array(
       "verify_peer"=>false,
       "verify_peer_name"=>false,
    ),
	'http' => array(
		'header' => "Content-Type: application/x-www-form-urlencoded\r\n".
                    "Content-Length: ".strlen($data)."\r\n",	
		'method'  => 'POST',
		'content' => $data
	)
);
//Lectura de un archivo JSON desde una URL
$json = file_get_contents($url,false, stream_context_create($arrContextOptions));
//Decodificacion del archiv JSON
$obj = json_decode($json);
if(count($obj->data->agrobiodiversidads) > 0){
	$elimina = "DELETE FROM catalogocentralizado.RelNombreCatalogo WHERE IdCatNombre = 2386";
	if ($conn->query($elimina) === TRUE) {
	}else{
		echo "<font color='red' >Error updating record: </font><br>" . $conn->error;
	}
	//Consulta de insercion de datos 
	$psql = "INSERT INTO catalogocentralizado.RelNombreCatalogo(IdNombre, IdCatNombre, Observaciones) VALUES";
	foreach($obj->data->agrobiodiversidads as $nombres){
		//Consultamos el IdNombre a partir del IdCAT que nos devuelve el WS
		$sql = "SELECT IdNombre FROM catalogocentralizado.SCAT where IdCAT = '".$nombres->id."';";
		$result = $conn->query($sql);
		$idAgro = 0;
		while($row = $result->fetch_assoc()) {
			//armamos cada uno de los insert
			$psql .= "(".$row["IdNombre"].",2386,'Origen:SIAGRO-API'),";
			$idAgro = $row["IdNombre"];
		}
		$sqlAgro = "SELECT COUNT(1) as encontrado FROM catalogocentralizado.RelNombreCatalogo WHERE IdNombre = ".$idAgro." AND IdCatNombre = 2385";
		$resultAgro = $conn->query($sqlAgro);
		$noAgro = false;
		while($rowAgro = $resultAgro->fetch_assoc()) {
			//Validamos si el Id ya se encuentra en la tabla
			if($rowAgro["encontrado"] == 0){
				$noAgro = true;
			}
		}
		if($noAgro){
			$insertAgro = "INSERT INTO catalogocentralizado.RelNombreCatalogo (IdNombre, IdCatNombre, Observaciones) VALUES
			(".$idAgro.",2385,'Origen:SIAGRO-API');";
			if ($conn->query($insertAgro) === TRUE) {
			}else{
				echo "<font color='red' >Error updating record: </font><br>" . $conn->error;
			}
		}
	}
	
	if ($conn->query(substr($psql,0,strlen($psql)-1)) === TRUE) {
	}else{
		echo "<font color='red' >Error updating record: </font><br>" . $conn->error;
	}
}
else { exit; }
$conn->close();
echo "Termine";
?>
