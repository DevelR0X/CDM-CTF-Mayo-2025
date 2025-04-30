<?php
/**
 * name....: Challenge XSS WAF Bypass 
 * author..: Esteban XFCE - Develrox
 * date....: 04-2025
 * 
 **/

class PCRDatabase
{
    private $db;

    public function __construct($databaseFile = "database.db")
    {
        $this->db = new PDO("sqlite:" . $databaseFile);
        $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $this->initializeDatabase();
        $this->setDefaultData();
    }

    private function initializeDatabase()
    {
        $sql = "
            CREATE TABLE IF NOT EXISTS pcr_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                folio TEXT NOT NULL,
                resultado TEXT NOT NULL
            )
        ";
        $this->db->exec($sql);
    }

    private function setDefaultData()
    {
        $result = $this->db->query("SELECT COUNT(*) FROM pcr_results");
        $count  = $result->fetchColumn();

        if ($count == 0) {
            for($i=0; $i<15; $i++) {
                $date      = date("d-m-Y H:i:s");
                $folio     = sprintf("PCR-%d-%d", rand(100000, 999999), time());
                $resultado = rand(0, 1) ? 'POSITIVO' : 'NEGATIVO';

                $this->insertTest($date, $folio, $resultado);
            }
        }
    }

    public function insertTest(
        string $fecha,
        string $folio,
        string $resultado
    ): void {
        $sql = "
            INSERT INTO pcr_results (fecha, folio, resultado)
            VALUES (:fecha, :folio, :resultado)
        ";
        $stmt = $this->db->prepare($sql);
        $stmt->bindValue(":fecha", $fecha, PDO::PARAM_STR);
        $stmt->bindValue(":folio", $folio, PDO::PARAM_STR);
        $stmt->bindValue(":resultado", $resultado, PDO::PARAM_STR);
        $stmt->execute();
    }

    public function getTests(int $page = 1, int $pageSize = 10): array
    {
        $offset = ($page - 1) * $pageSize;
        $sql = "
            SELECT fecha, folio, resultado
            FROM pcr_results
            ORDER BY id DESC
            LIMIT :limit OFFSET :offset
        ";
        $stmt = $this->db->prepare($sql);
        $stmt->bindValue(":limit", $pageSize, PDO::PARAM_INT);
        $stmt->bindValue(":offset", $offset, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}

?>
